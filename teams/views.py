from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.request import Request
from django.forms.models import model_to_dict

from .models import Team
from .utils import data_processing
from .exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError


class TeamView(APIView):
    def get(self, request: Request):
        teams = Team.objects.all()

        teams_list = [model_to_dict(i) for i in teams]

        return Response(teams_list, status.HTTP_200_OK)

    def post(self, request: Request):
        try:
            new_team = data_processing(request.data)
        except NegativeTitlesError as error:
            return Response({"error": error.message}, status.HTTP_400_BAD_REQUEST)
        except InvalidYearCupError as error:
            return Response({"error": error.message}, status.HTTP_400_BAD_REQUEST)
        except ImpossibleTitlesError as error:
            return Response({"error": error.message}, status.HTTP_400_BAD_REQUEST)

        created_team = Team.objects.create(**new_team)

        team_dict = model_to_dict(created_team)

        return Response(team_dict, status.HTTP_201_CREATED)


class TeamDetailView(APIView):
    def get(self, request: Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def patch(self, request: Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        for keys, values in request.data.items():
            setattr(team, keys, values)

        team.save()

        team_dict = model_to_dict(team)

        return Response(team_dict, status.HTTP_200_OK)

    def delete(self, request: Request, team_id):
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status.HTTP_404_NOT_FOUND)

        team.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
