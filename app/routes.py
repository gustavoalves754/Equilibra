"""Rotas básicas da API do Equilibra."""
 
from flask import Blueprint, jsonify
 
api = Blueprint("api", __name__)
 
 
@api.get("/")

def home():

    """Retorna a identificação da API."""

    return jsonify(

        {

            "name": "Equilibra API",

            "version": "1.0",

        }

    ), 200
 
 
@api.get("/health")

def health():

    """Verifica se a API está funcionando."""

    return jsonify(

        {

            "status": "ok",

        }

    ), 200