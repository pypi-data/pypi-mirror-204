""" Creates a WSGI app """
from webservice import HomeServices, initialize_debugger

def create_app():
    """
        Instantiate a flask webservice to be served as a wsgi
    Returns:
        WSGI app
    """
    initialize_debugger()

    #templates_path = "{}/templates".format(Path().absolute())
    #static_path = "{}/static".format(Path().absolute())
    templates_path = None
    static_path = None
    wtf_service = HomeServices(template_folder=templates_path, static_folder=static_path)
    return wtf_service.get_app()


if __name__ == '__main__':
    create_app = create_app()
    create_app.run(host='0.0.0.0')  # host='0.0.0.0' so that its detected from the outside
