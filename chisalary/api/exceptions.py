from rest_framework.exceptions import APIException


class ChicagoDataPortalError(APIException):
    status_code = 503
    default_detail = 'Chicago Data Portal is not available, please check that the portal is up and running.'
    default_code = 'data_portal_unavailable'
