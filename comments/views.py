from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Comment
from .serializers import (
    RecursiveCommentSerializer
)
from .services import (
    create_comment,
    soft_delete_comment
)


class CreateCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        comment = create_comment(
            ticket_id=request.data.get("ticket"),
            user=request.user,
            content=request.data.get("content"),
            parent_id=request.data.get("parent")
        )

        serializer = RecursiveCommentSerializer(
            comment
        )

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class TicketCommentsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):

        comments = Comment.objects.filter(
            ticket_id=ticket_id,
            parent=None,
            is_deleted=False
        )

        serializer = RecursiveCommentSerializer(
            comments,
            many=True
        )

        return Response(serializer.data)


class UpdateCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, comment_id):

        comment = Comment.objects.get(
            id=comment_id
        )

        if comment.user != request.user:

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        comment.content = request.data.get(
            "content",
            comment.content
        )

        comment.save()

        serializer = RecursiveCommentSerializer(
            comment
        )

        return Response(serializer.data)


class DeleteCommentView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):

        comment = Comment.objects.get(
            id=comment_id
        )

        if comment.user != request.user:

            return Response(
                {"error": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        soft_delete_comment(comment=comment)

        return Response({
            "message": "Comment deleted"
        })