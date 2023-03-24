import argparse
import os
import socket
import threading

import cv2
import pickle
import struct

import Logger

def load_env():
    if not os.path.exists('.env') and not os.path.exists('../.env'):
        Logger.error('Could not find any .env in the current or parent folder!')
        return dict()

    result = dict()

    # Load text content
    env_text = ''
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_text = f.readlines()

    if len(env_text) == 0 and os.path.exists('../.env'):
        with open('../.env', 'r') as f:
            env_text = f.readlines()

    if len(env_text) == 0:
        Logger.error('Could not load env file!')
        return dict()

    for line in env_text:
        if line == '\n':
            continue

        if line.endswith('\n'):
            line = line.strip('\n')

        key_value_pairs = line.split('=')
        key = key_value_pairs[0]
        value = key_value_pairs[1]

        result[key] = value

    return result

def on_client_connected(conn, addr, output_video_path):
    print(f'New client connected through address {addr}!')

    connected = True
    video_frames = []

    # TODO: receive from client in init phase
    frame_width = 640
    frame_height = 480

    payload_size = struct.calcsize("L")
    data = b''
    while connected:
        msg = conn.recv(64)
        if msg is None:
            continue

        print(msg)
        msg = msg.decode('utf-8')
        if len(msg) > 0:
            print(msg)

        if msg == 'join':
            print('Client wants to connect...')
        elif msg == 'leave':
            data = ""
            print('Client wants to disconnect...')
            connected = False

            # store video
            print(f'Saving stream to {output_video_path}...')

        #    with open(f'{output_video_path}/filename.mp4', 'wb') as f:
        #        print(len(video_frames))
        #        for frame in video_frames:
        #            f.write(frame)


            out = cv2.VideoWriter(f'{output_video_path}/filename.mp4', cv2.VideoWriter_fourcc(*'MP4V'),
                                     30, (frame_width, frame_height))

            for image in video_frames:
                out.write(image)

            out.release()

        elif msg == 'stream':
            print('Client sends more stream data...')

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

            video_frames.append(frame)

    conn.close()


def main(output_video_path, verbose_logging, envs):
    print('Running server and using ' + output_video_path + ' as the video output path...')
    if verbose_logging:
        print('Verbose logging enabled.')

    server_address = envs['SERVER_ADDRESS']
    server_port = int(envs['SERVER_PORT'])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen()
    Logger.info(f'Listening at {server_address}:{server_port}...')

    while True:
        conn, addr = server_socket.accept()
        client_thread = threading.Thread(target=on_client_connected, args=[conn, addr, output_video_path])
        client_thread.start()

    print('Shutting down main application...')

def run_cli(output_video_path, vervose_logging, envs):
    print('Starting command line interface...')


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
    envs = load_env()
    if args.verbose:
        Logger.debug(envs)

    if args.with_command_line_interface:
        run_cli(args.video_path, args.verbose, envs)
    else:
        main(args.video_path, args.verbose, envs)
