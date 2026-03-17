from flask import Flask, request, jsonify, render_template
import yaml
import os

app = Flask(__name__)

# Chemins des fichiers
PANEL_CONFIG_PATH = 'examples/panelConfig.yaml'
SITE_CONFIG_PATH = 'examples/siteConfig.yaml'
SVG_PATH = 'test.svg'
XML_PATH = 'test.xml'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    try:
        with open(PANEL_CONFIG_PATH, 'r', encoding='utf-8') as f:
            panel_config = yaml.safe_load(f)
        with open(SITE_CONFIG_PATH, 'r', encoding='utf-8') as f:
            site_config = yaml.safe_load(f)
        return jsonify({
            'panelConfig': panel_config,
            'siteConfig': site_config
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['POST'])
def save_config():
    try:
        data = request.json
        if 'panelConfig' in data:
            with open(PANEL_CONFIG_PATH, 'w', encoding='utf-8') as f:
                yaml.dump(data['panelConfig'], f, allow_unicode=True, sort_keys=False)
        if 'siteConfig' in data:
            with open(SITE_CONFIG_PATH, 'w', encoding='utf-8') as f:
                yaml.dump(data['siteConfig'], f, allow_unicode=True, sort_keys=False)
        return jsonify({'message': 'Configuration sauvegardée avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
