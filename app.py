from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projects.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/')
def index():
    db.create_all()
    if not Project.query.first():
        projects = [Project(name=name) for name in ["Everlasting Bitterballen", "Stroopwafel Printer", "ZouteDrop Canals",  "Chocolate sprinkles bath", "Hot Ice Cream", "To Delete"]]
        db.session.bulk_save_objects(projects)
        db.session.commit()
    project_names = [project.name for project in Project.query.all()]
    return "<h1>Highly prioritized projects (˘▾˘):</h1>\n<ul>" + '\n'.join('<li>◆ ' + name + ' ◆</li>' for name in project_names) + "</ul>"


@app.route('/updated', methods=['POST'])
def add_project(new_name=None):
    if new_name is None:
        data = request.get_json()
        new_name = data.get('name')
    if not new_name:
        return jsonify({"message": "Missing new name for the project"}), 400
    if Project.query.filter_by(name=new_name).first():
        return jsonify({"message": "Project already exists"}), 409
    new_project = Project(name=new_name)
    db.session.add(new_project)
    db.session.commit()
    return jsonify({"message": "Project added successfully", "project": {"id": new_project.id, "name": new_project.name}}), 201


@app.route('/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([{"id": project.id, "name": project.name} for project in projects]), 200

@app.route('/projects/<int:id>', methods=['PUT'])
def update_project(id, new_name=None):
    if new_name is None:
        data = request.get_json()
        new_name = data.get('name')
    if not new_name:
        return jsonify({"message": "Missing new name for the project"}), 400
    project = db.session.get(Project, id)
    if not project:
        return jsonify({"message": "Project not found"}), 404
    project.name = new_name
    db.session.commit()
    return jsonify({"message": "Project updated"}), 200

@app.route('/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = db.session.get(Project, id)
    if not project:
        return jsonify({'message': 'Project not found'}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message': 'Project deleted'}), 200

if __name__ == '__main__':
    with app.app_context():
        add_project('DecisionMaker: Kibbeling or Herring')
        update_project(5, "COLD ICE CREAM")
        delete_project(6)
    app.run(debug=True, port=5001)