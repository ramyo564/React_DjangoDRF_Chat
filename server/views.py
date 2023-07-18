from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from django.db.models import Count
from .models import Server
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    """
    ViewSet for retrieving a list of servers with various filtering options.

    Parameters:
        - category (str, optional): Filter servers by category name.
        - qty (int, optional): Limit the number of servers returned.
        - by_user (bool, optional): Filter servers by the authenticated user (True) or all users (False).
        - by_serverid (int, optional): Filter servers by their unique identifier.
        - with_num_members (bool, optional): Include the count of members for each server (True) or not (False).

    Raises:
        - AuthenticationFailed: If 'by_user' or 'by_serverid' is True and the user is not authenticated.
        - ValidationError: If 'by_serverid' is provided but the server with the given ID does not exist.

    Returns:
        - Response: A list of servers with optional member count if 'with_num_members' is True.

    Example:
        To retrieve a list of servers belonging to the authenticated user:
        ```
        GET /api/servers/?by_user=true
        ```

        To retrieve the first 5 servers in a specific category with member count:
        ```
        GET /api/servers/?category=example&qty=5&with_num_members=true
        ```

        To retrieve a server with a specific ID:
        ```
        GET /api/servers/?by_serverid=12345
        ```
    """
    queryset = Server.objects.all()
    
def list(self, request):
    """
    Retrieve a list of servers based on the provided filtering options.

    This method allows you to filter and retrieve a list of servers based on various criteria.

    Args:
        request (rest_framework.request.Request): The request object containing query parameters.

    Returns:
        rest_framework.response.Response: A serialized list of servers.

    Raises:
        rest_framework.exceptions.AuthenticationFailed:
            If 'by_user' or 'by_serverid' is True and the user is not authenticated.
        rest_framework.exceptions.ValidationError:
            If 'by_serverid' is provided but the server with the given ID does not exist.

    Filtering Options:
        - category (str, optional): Filter servers by category name.
        - qty (int, optional): Limit the number of servers returned.
        - by_user (bool, optional): Filter servers by the authenticated user (True) or all users (False).
        - by_serverid (int, optional): Filter servers by their unique identifier.
        - with_num_members (bool, optional): Include the count of members for each server (True) or not (False).

    Example:
        1. Retrieve a list of servers belonging to the authenticated user:
        ```
        GET /api/servers/?by_user=true
        ```

        2. Retrieve the first 5 servers in a specific category with member count:
        ```
        GET /api/servers/?category=example&qty=5&with_num_members=true
        ```

        3. Retrieve a server with a specific ID:
        ```
        GET /api/servers/?by_serverid=12345
        ```

    Note:
        The queryset for filtering the servers is derived from the 'Server' model and should be defined
        in the 'queryset' attribute of the 'ServerListViewSet' class.

    Important:
        - The 'by_user' and 'by_serverid' options are mutually exclusive. If both are provided, 'by_user' takes precedence.
        - 'by_user' option requires authentication. If not authenticated and 'by_user' is True, an AuthenticationFailed exception will be raised.
        - 'by_serverid' option filters servers based on their unique identifier. If a server with the provided ID does not exist,
          a ValidationError will be raised.

    Performance Considerations:
        - Using 'with_num_members=True' to include member counts may impact response time, especially for large datasets.
        - Avoid using 'qty' with a large value when the queryset contains a large number of servers, as it may result in longer processing times.

    Security Considerations:
        - Ensure that only authorized users have access to this endpoint to prevent unauthorized access to sensitive server data.
        - Validate and sanitize input parameters to prevent potential security vulnerabilities like SQL injection or other attacks.

    Returns:
        rest_framework.response.Response: A serialized list of servers matching the specified filtering options.
    """
    category = request.query_params.get("category")
    qty = request.query_params.get('qty')
    by_user = request.query_params.get('by_user') == "true"
    by_serverid = request.query_params.get("by_serverid")
    with_num_members = request.query_params.get('with_num_members') == "true"
    
    # Check for authentication if 'by_user' or 'by_serverid' is True
    if by_user or (by_serverid and not request.user.is_authenticated):
        raise AuthenticationFailed()
    
    # Apply category filter if provided
    if category:
        self.queryset = self.queryset.filter(category__name=category)
            
    # Filter servers by the authenticated user
    if by_user:
        user_id = request.user.id
        self.queryset = self.queryset.filter(member=user_id)
        
    # Annotate the count of members if 'with_num_members' is True
    if with_num_members:
        self.queryset = self.queryset.annotate(num_members=Count("member"))
        
    # Limit the number of servers returned if 'qty' is provided
    if qty:
        self.queryset = self.queryset[: int(qty)]

    # Filter servers by the provided server ID
    if by_serverid:
        try:
            self.queryset = self.queryset.filter(id=by_serverid)
            if not self.queryset.exists():
                raise ValidationError(detail=f"Server with ID {by_serverid} not found")
        except ValueError:
            raise ValidationError(detail="Invalid server ID")

    # Serialize the queryset and return the response
    serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_members})
    return Response(serializer.data)