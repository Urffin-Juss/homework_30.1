from rest_framework.permissions import BasePermission

class IsOwnerOrModerator(BasePermission):
    """
    Модератор: может читать/редактировать любые Course/Lesson, но НЕ может создавать и удалять.
    Обычный пользователь: может CRUD только своих объектов.
    """

    def is_moderator(self, user):
        return user.is_authenticated and user.groups.filter(name="moderators").exists()

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if self.is_moderator(request.user):
            # модератору запрещаем create/delete
            if request.method in ("POST", "DELETE"):
                return False
            return True

        return True  # обычный юзер — дальше решит object permission

    def has_object_permission(self, request, view, obj):
        user = request.user
        if self.is_moderator(request.user):
            # модератор может читать/менять, но не удалять
            if request.method == "DELETE":
                return False
            return True

        return getattr(obj, "owner_id", None) == request.user.id