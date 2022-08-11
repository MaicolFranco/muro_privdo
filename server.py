from flask_app import app
#ACA SE TIENEN QUE IMPORTAR LOS CONTROLADORES
from flask_app.controllers import users_controller, messages_controller





if __name__=="__main__":
    app.run(debug=True)