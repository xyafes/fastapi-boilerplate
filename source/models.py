from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    user_id = fields.IntField(unique=True, null=False)
    username = fields.CharField(max_length=255, unique=True, null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    def __str__(self):
        return self.username


class UserMessage(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField(
        "models.User",
        related_name="messages",
        on_delete=fields.CASCADE,
    )
    message = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.message