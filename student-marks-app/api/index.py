from http.server import BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Enable CORS
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        # Parse query parameters
        query_params = self.path.split('?')[1] if '?' in self.path else ''
        names = self.parse_query_params(query_params)

        # Load student data
        with open('students.json', 'r') as f:
            students = json.load(f)

        # Fetch marks for the requested names
        marks = [students.get(name, None) for name in names]

        # Prepare response
        response = {
            "marks": marks
        }

        # Send response
        self.wfile.write(json.dumps(response).encode())

    def parse_query_params(self, query_string):
        from urllib.parse import parse_qs
        params = parse_qs(query_string)
        return params.get('name', [])

# This is required for Vercel to recognize the handler
def handler(event, context):
    return Handler().do_GET()