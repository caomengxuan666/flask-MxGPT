from gevent import pywsgi
import argparse
from route import app


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask application.')
    # 默认参数
    parser.add_argument('--mode', choices=['local', 'server'], default='local',
                        help='Running mode: "local" for development (default), "server" for production.')

    args = parser.parse_args()

    if args.mode == 'local':
        print("Running in local development mode...")
        app.run(debug=True)
    elif args.mode == 'server':
        print("Running in production server mode...")
        # 使用gevent的WSGIServer来提高性能
        server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
        server.serve_forever()
