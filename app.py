from flask import Flask, request, jsonify, render_template
import yaml
import os

app = Flask(__name__)

# Chemins des fichiers
PANEL_CONFIG_PATH = 'test/panelConfig.yaml'
SITE_CONFIG_PATH = 'test/siteConfig.yaml'
SVG_PATH = 'test/test.svg'
XML_PATH = 'test/test.xml'

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
            panel_cfg = data['panelConfig']
            # Nettoyage pour éviter l'erreur TypeError: n.thresholdPatterns.forEach is not a function
            if 'cells' in panel_cfg:
                for cell_name, cell_data in panel_cfg['cells'].items():
                    if 'labelColor' in cell_data and 'thresholdPatterns' in cell_data['labelColor']:
                        # On supprime thresholdPatterns s'il est vide ou si un thresholdPatternsRef est utilisé
                        # Grafana s'attend à un tableau s'il est présent
                        if not cell_data['labelColor']['thresholdPatterns'] or cell_data['labelColor'].get('thresholdPatternsRef'):
                            del cell_data['labelColor']['thresholdPatterns']
                    if 'fillColor' in cell_data and 'thresholdPatterns' in cell_data['fillColor']:
                        if not cell_data['fillColor']['thresholdPatterns'] or cell_data['fillColor'].get('thresholdPatternsRef'):
                            del cell_data['fillColor']['thresholdPatterns']
                    if 'strokeColor' in cell_data and 'thresholdPatterns' in cell_data['strokeColor']:
                        if not cell_data['strokeColor']['thresholdPatterns'] or cell_data['strokeColor'].get('thresholdPatternsRef'):
                            del cell_data['strokeColor']['thresholdPatterns']

            with open(PANEL_CONFIG_PATH, 'w', encoding='utf-8') as f:
                yaml.dump(panel_cfg, f, allow_unicode=True, sort_keys=False)
        if 'siteConfig' in data:
            with open(SITE_CONFIG_PATH, 'w', encoding='utf-8') as f:
                yaml.dump(data['siteConfig'], f, allow_unicode=True, sort_keys=False)
        return jsonify({'message': 'Configuration sauvegardée avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
