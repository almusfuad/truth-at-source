from rest_framework.permissions import BasePermission


class IsFactory(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'factory'
    

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'buyer'
    

    