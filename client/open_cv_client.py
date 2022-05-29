import os
import time
import argparse
import socketio
import cv2
import base64

stream_server = os.environ.get('LIVE_STREAM_SERVER') or '20.124.101.32'
stream_port = os.environ.get('LIVE_STREAM_PORT') or 80

sio = socketio.Client()

@sio.event
def connect():
    print('[INFO] Successfully connected to server.')

@sio.event
def connect_error():
    print('[INFO] Failed to connect to server.')

@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')


class OpenCVStreamer(object):
    def __init__(self, server_addr=stream_server, server_port=stream_port, stream_fps=20.0):
        self.server_addr = server_addr
        self.server_port = server_port
        self._stream_fps = stream_fps
        self._last_update_t = time.time()
        self._wait_t = (1/self._stream_fps)

    def setup(self):
        print('[INFO] Connecting to server http://{}:{}...'.format(
            self.server_addr, self.server_port))
        sio.connect(
                'http://{}:{}'.format(self.server_addr, self.server_port),
                transports=['websocket'],
                namespaces=['/', '/cv'])

        time.sleep(1)
        return self

    def _convert_image_to_jpeg(self, image):
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)

    def send_data(self, frame, text):
        cur_t = time.time()
        if cur_t - self._last_update_t > self._wait_t:
            self._last_update_t = cur_t
            frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))
            sio.emit(
                    'cv2server',
                    {
                        'image': self._convert_image_to_jpeg(frame),
                        'text': '<br />'.join(text)
                    })

    def check_exit(self):
        pass

    def close(self):
        sio.disconnect()


def main(camera, server_addr, server_port, stream_fps):

    # Open streamer
    streamer = OpenCVStreamer(server_addr, server_port, stream_fps).setup()

    try:

        video = cv2.VideoCapture(camera)

        frame_idx = 0
        start_time = time.time()
        while True:
            ret, frame = video.read()
            frame = cv2.flip(frame, 1)
            frame_idx += 1
            cur_time = time.time()
            duration = cur_time - start_time
            fps = round(frame_idx/duration, 2)
            fps_text = ['FPS: {}'.format(fps)]
            streamer.send_data(frame, fps_text)
            # print('Send frame ({}): {}'.format(frame_idx, fps_text))

            if streamer.check_exit():
                break

    except Exception as ex:
        print('Exceception: {}'.format(ex))

    finally:
        if streamer is not None:
            streamer.close()
        print("Program Done.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Visionify Video Streamer')
    parser.add_argument(
            '--camera', type=int, default='0',
            help='The camera index to stream from.')
    parser.add_argument(
            '--server-addr',  type=str, default=stream_server,
            help='The IP address or hostname of the SocketIO server.')
    parser.add_argument(
            '--server-port',  type=int, default=stream_port,
            help='The Port number for where this is hosted.')
    parser.add_argument(
            '--stream-fps',  type=float, default=20.0,
            help='The rate to send frames to the server.')
    args = parser.parse_args()
    main(args.camera, args.server_addr, args.server_port, args.stream_fps)
