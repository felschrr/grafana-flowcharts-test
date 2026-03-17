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
            # Nettoyage pour éviter les erreurs TypeError: forEach is not a function sur Grafana
            if 'cells' in panel_cfg:
                for cell_name, cell_data in panel_cfg['cells'].items():
                    # Nettoyage des thresholdPatterns
                    for attr in ['labelColor', 'fillColor', 'strokeColor']:
                        if attr in cell_data:
                            # Supprime thresholdPatterns s'il est vide ou si un thresholdPatternsRef est utilisé
                            if 'thresholdPatterns' in cell_data[attr]:
                                if not cell_data[attr]['thresholdPatterns'] or cell_data[attr].get('thresholdPatternsRef'):
                                    del cell_data[attr]['thresholdPatterns']
                            
                            # Correction pour labelColorCompound, fillColorCompound, strokeColorCompound
                            # Grafana attend un tableau dans 'colors' s'il est défini. 
                            # Si c'est "..." (valeur par défaut de l'exemple) ou vide, on le supprime.
                            compound_attr = f"{attr}Compound"
                            if compound_attr in cell_data:
                                if 'colors' in cell_data[compound_attr]:
                                    colors = cell_data[compound_attr]['colors']
                                    if colors == "..." or not colors:
                                        del cell_data[compound_attr]

            with open(PANEL_CONFIG_PATH, 'w', encoding='utf-8') as f:
                f.write('---\n')
                yaml.dump(panel_cfg, f, allow_unicode=True, sort_keys=False)
        if 'siteConfig' in data:
            with open(SITE_CONFIG_PATH, 'w', encoding='utf-8') as f:
                f.write('---\n')
                yaml.dump(data['siteConfig'], f, allow_unicode=True, sort_keys=False)
        return jsonify({'message': 'Configuration sauvegardée avec succès'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
