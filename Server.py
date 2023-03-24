import argparse
import os
import socket
import sys
import threading

import multiprocessing
from threading import Lock

import cv2
import pickle
import struct

import Logger
import EnvironmentLoader

CAMERA_CLIENTS = {} # map ADDR -> frames
CAMERA_DISPLAYS = {} # map ADDR -> conn
CAMERA_THREADS = {} # map ADDR -> thread

# determines, whether the server should continue listening for new clients
# should be changeable through the CLI
ACCEPT_CLIENTS = True

def on_client_connected(conn, addr, output_video_path, thread_lock):
    """
    This function handles the connected clients and runs in its own thread.
    """
    global CAMERA_CLIENTS
    global CAMERA_DISPLAYS

    Logger.success(f'New client connected through address {addr}!')

    connected = True
    #video_frames = []

    # TODO: receive from client in init phase
    frame_width = 640
    frame_height = 480

    payload_size = struct.calcsize("L")
    data = b''
    while connected:
        msg = conn.recv(64)
        if msg is None:
            continue

        try:
            msg = msg.decode('utf-8')
            if len(msg) > 0:
                Logger.debug(f'{addr}: {msg}')
        except Exception as e:
            # The initial message is not a string
            Logger.warn('Unhandled 64 bytes!!!')
            continue

        if msg == 'join':
            Logger.info(f'{addr}: Client wants to connect...')
        elif msg == 'camera':
            Logger.info(f'{addr}: registered as CAMERA.')
            # initialize the map with the current address, so that later this entry can be filled with frames.
            thread_lock.acquire()
            CAMERA_CLIENTS[addr] = []
            thread_lock.release()
        elif msg == 'display':
            Logger.info(f'{addr}: registered as DISPLAY.')

            # store the connection for later, when broadcasting all frames to this client.
            thread_lock.acquire()
            CAMERA_DISPLAYS[addr] = conn
            thread_lock.release()
        elif msg == 'leave':
            data = ""
            Logger.info(f'{addr}: Client wants to disconnect...')
            connected = False

            # store video
            Logger.info(f'Saving stream to {output_video_path}/filename.mp4...')
            out = cv2.VideoWriter(f'{output_video_path}/filename.mp4', cv2.VideoWriter_fourcc(*'MP4V'),
                                     30, (frame_width, frame_height))

            for image in CAMERA_CLIENTS[addr]:
                out.write(image)

            out.release()

        elif msg == 'stream':
            Logger.info(f'{addr}: Client sends stream data...')

            while len(data) < payload_size:
                data += conn.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += conn.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)

        #    cv2.imshow('Server frame', frame)
        #    cv2.waitKey(1)

            thread_lock.acquire()
            CAMERA_CLIENTS[addr].append(frame)
            thread_lock.release()

        # TODO: broadcast to every display the current frames of every camera
        for display_address, display_connection in CAMERA_DISPLAYS:
            # TODO: iterate over all camera clients and send their frames, maybe all packed into one message?
            for camera_address, camera_frames in CAMERA_CLIENTS:
                pass

    conn.close()


def main(output_video_path, verbose_logging, envs):
    """
    This is the global main function, that executes the server and listens for new connections.
    If the CLI is enabled, this function runs in its own process, otherwise it runs on the main process.
    """
    global ACCEPT_CLIENTS

    Logger.success('Running server and using ' + output_video_path + ' as the video output path...')
    if verbose_logging:
        Logger.success('Verbose logging enabled.')

    server_address = envs['SERVER_ADDRESS']
    server_port = int(envs['SERVER_PORT'])

    thread_lock = Lock()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen()
    Logger.info(f'Listening at {server_address}:{server_port}...')

    while True:
        if not ACCEPT_CLIENTS:
            Logger.info('Application requested to shutdown')
            break

        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=on_client_connected, args=[conn, addr, output_video_path, thread_lock])
        CAMERA_THREADS[addr] = client_thread
        client_thread.start()

    # TODO: find a better solution for this
    #       if CLI is enabled and the application requested to shutdown, the process gets killed
    #       so this will never be called...
    Logger.info('Shutting down main application...')
    for camera_addr, thread in CAMERA_THREADS:
        thread.join()


def cli_main(conn, new_fd):
    """
    The main function for the CLI, which runs in its own process.
    """
    sys.stdin = os.fdopen(new_fd)

    while True:
        try:
            text = input('CLI > ')
        except KeyboardInterrupt as e:
            break

        if text.lower() == 'version':
            Logger.info(f'Version: 1.0.0')
        elif text.lower() == 'quit':
            # Stop the other thread too, which is listening for new connections
            conn.send(False)
            conn.close()
            break

def run_cli(output_video_path, verbose_logging, envs):
    """
    starter function for the CLI, which is still executed on the main process.
    """
    global ACCEPT_CLIENTS
    Logger.success('Starting command line interface...')

    main_process = multiprocessing.Process(target=main, args=[output_video_path, verbose_logging, envs])
    main_process.start()

    parent_conn, child_conn = multiprocessing.Pipe()
    cli_process = multiprocessing.Process(target=cli_main, args=(child_conn, sys.stdin.fileno()))
    cli_process.start()

    try:
        # receive, whether to continue accepting clients
        ACCEPT_CLIENTS = parent_conn.recv()
    except KeyboardInterrupt as e:
        # hard shutdown
        cli_process.kill()
        main_process.kill()

    if not ACCEPT_CLIENTS:
        Logger.info('Shutting down the server...')
        main_process.kill()

    Logger.info('Shutting down the CLI...')
    cli_process.kill()


if __name__ == '__main__':
    # handle program arguments first
    parser = argparse.ArgumentParser(description='This program acts as the CamServer, '
                                                 'receiving the data stream from camera client applications and '
                                                 'storing them onto the webserver.')
    parser.add_argument('video_path', help='The Output path, where the received camera feeds should be stored to.')
    parser.add_argument('-w-cli', '--with-command-line-interface', action='store_true', help='Enable the command '
                                                                                             'line interface')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose logging')
    args = parser.parse_args()

    # load environment file
    envs = EnvironmentLoader.load()
    if args.verbose:
        Logger.enableDebugger()
        Logger.debug(envs)

    if args.with_command_line_interface:
        run_cli(args.video_path, args.verbose, envs)
    else:
        main(args.video_path, args.verbose, envs)
