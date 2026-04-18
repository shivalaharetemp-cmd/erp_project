from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import logout as django_logout
from .models import Company, User, CompanyUser
from .serializers import (
    LoginSerializer, UserSerializer, ChangePasswordSerializer,
    CompanySerializer, CompanySelectSerializer, CompanyContextSerializer,
)
from audit.services import AuditService


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Log login
        AuditService.log(
            user=user, company=None, action='LOGIN',
            model_name='User', object_id=str(user.id),
            request=request,
        )

        return Response({
            'user': UserSerializer(user).data,
            'token': user.auth_token.key if hasattr(user, 'auth_token') else None,
        })


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        AuditService.log(
            user=request.user, company=None, action='LOGOUT',
            model_name='User', object_id=str(request.user.id),
            request=request,
        )
        django_logout(request)
        return Response({'detail': 'Successfully logged out.'})


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'detail': 'Password changed successfully.'})


class UserCompaniesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Get companies accessible to the current user."""
        company_users = CompanyUser.objects.filter(
            user=request.user, is_active=True
        ).select_related('company')
        companies = []
        for cu in company_users:
            company_data = CompanySerializer(cu.company).data
            company_data['role'] = cu.role
            companies.append(company_data)
        return Response(companies)


class SelectCompanyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CompanySelectSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        company_id = str(serializer.validated_data['company_id'])

        request.session['company_id'] = company_id

        company = Company.objects.get(id=company_id)
        cu = CompanyUser.objects.get(user=request.user, company=company)
        AuditService.log(
            user=request.user, company=company,
            action='SELECT_COMPANY', model_name='Company',
            object_id=company_id, request=request,
        )

        return Response({
            'detail': 'Company selected successfully.',
            'company_id': company_id,
            'company_name': company.name,
        })


class CompanyContextView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        company_id = request.session.get('company_id')
        if not company_id:
            return Response({'error': 'No company selected.'}, status=400)

        try:
            company = Company.objects.get(id=company_id)
            cu = CompanyUser.objects.get(user=request.user, company=company)
        except (Company.DoesNotExist, CompanyUser.DoesNotExist):
            return Response({'error': 'Company not found.'}, status=404)

        return Response(CompanyContextSerializer({
            'company_id': company.id,
            'company_name': company.name,
            'company_code': company.code,
            'user_role': cu.role,
            'financial_year': company.financial_year,
        }).data)


class CompanyListView(generics.ListAPIView):
    """Admin: List all companies."""
    serializer_class = CompanySerializer
    queryset = Company.objects.all()
    permission_classes = [permissions.IsAuthenticated]
