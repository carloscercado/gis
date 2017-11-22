from rest_framework import routers

class RaizAPI(routers.APIRootView):
    """
    Raiz del API
    """
    pass


class RaizRouter(routers.DefaultRouter):
    APIRootView = RaizAPI