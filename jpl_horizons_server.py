#!/usr/bin/env python3
"""
JPL Horizons API Server
A simple Flask server to proxy requests to JPL Horizons API without CORS issues
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/horizons', methods=['GET'])
def query_horizons():
    """
    Proxy endpoint for JPL Horizons API
    Accepts same query parameters as the JPL Horizons API
    """
    try:
        # Get all query parameters from the request
        params = dict(request.args)

        # JPL Horizons API endpoint
        horizons_url = 'https://ssd.jpl.nasa.gov/api/horizons.api'

        # Forward the request to JPL Horizons
        response = requests.get(horizons_url, params=params, timeout=30)

        if response.status_code != 200:
            return jsonify({
                'error': f'JPL Horizons API error: {response.status_code}',
                'details': response.text
            }), response.status_code

        # Return the response as plain text
        return response.text, 200, {'Content-Type': 'text/plain'}

    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request to JPL Horizons timed out'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request failed: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'JPL Horizons Proxy'}), 200

if __name__ == '__main__':
    print("="*70)
    print("JPL Horizons API Proxy Server")
    print("="*70)
    print("\nStarting server on http://localhost:5000")
    print("\nEndpoints:")
    print("  - http://localhost:5000/api/horizons  (Horizons API proxy)")
    print("  - http://localhost:5000/health        (Health check)")
    print("\nTo use with the web interface:")
    print("  1. Keep this server running")
    print("  2. Update jpl_horizons_lookup.html to use:")
    print("     const baseUrl = 'http://localhost:5000/api/horizons';")
    print("  3. Remove the CORS proxy code")
    print("\nPress Ctrl+C to stop the server")
    print("="*70)
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)
