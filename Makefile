APP_NAME := chat-message-processor-api
DOCKER_COMPOSE_FILE := docker-compose.yml

GREEN := \033[0;32m
NC := \033[0m

.PHONY: help build up down restart test lint install-deps run-local clean

help:
	@echo "${GREEN}Comandos disponibles:${NC}"
	@echo ""
	@echo "  ${GREEN}help${NC}           - Muestra esta ayuda."
	@echo "  ${GREEN}build${NC}          - Construye la imagen Docker de la aplicación."
	@echo "  ${GREEN}start${NC}          - Inicia los contenedores (construye la imagen si es necesario)."
	@echo "  ${GREEN}stop${NC}           - Detiene y elimina los contenedores."
	@echo "  ${GREEN}restart${NC}        - Reinicia los contenedores."
	@echo "  ${GREEN}test${NC}           - Ejecuta las pruebas unitarias y de integración dentro del contenedor."
	@echo "  ${GREEN}lint${NC}           - Ejecuta el linter (Flake8) dentro del contenedor."
	@echo "  ${GREEN}install-deps${NC}   - Instala las dependencias en el entorno virtual local."
	@echo "  ${GREEN}run-local${NC}      - Ejecuta la aplicación localmente (sin Docker)."
	@echo "  ${GREEN}clean${NC}          - Limpia el entorno (elimina entorno virtual, caché, etc.)."
	@echo ""

build:
	@echo "${GREEN}Construyendo la imagen Docker...${NC}"
	docker-compose -f $(DOCKER_COMPOSE_FILE) build

start: build
	@echo "${GREEN}Iniciando los contenedores...${NC}"
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

stop:
	@echo "${GREEN}Deteniendo y eliminando los contenedores...${NC}"
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

restart: down up
	@echo "${GREEN}Reiniciando los contenedores...${NC}"

test: build
	@echo "${GREEN}Ejecutando pruebas dentro del contenedor...${NC}"
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm app pytest

coverage:
	@echo "Generando reporte de cobertura de código..."
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm app pytest --cov=app tests/
	@echo "Reporte de cobertura de código generado en la consola.

lint: build
	@echo "${GREEN}Ejecutando linter (Flake8) dentro del contenedor...${NC}"
	docker-compose -f $(DOCKER_COMPOSE_FILE) run --rm app flake8 app tests

install-deps:
	@echo "${GREEN}Creando y activando entorno virtual...${NC}"
	python3$(PYTHON_VERSION) -m venv venv
	@echo "${GREEN}Activando entorno virtual e instalando dependencias...${NC}"
	@echo "Por favor, activa tu entorno virtual manualmente y ejecuta 'pip install -r requirements.txt'."
	@echo "Ej: source venv/bin/activate"
	@echo "Ej: pip install -r requirements.txt"

run-local: install-deps
	@echo "${GREEN}Ejecutando la aplicación localmente...${NC}"
	@echo "Por favor, activa tu entorno virtual y ejecuta 'uvicorn main:app --reload'."
	@echo "Ej: source venv/bin/activate"
	@echo "Ej: uvicorn main:app --reload"

clean:
	@echo "${GREEN}Limpiando entorno...${NC}"
	rm -rf venv
	rm -f *.db
	rm -rf instance/
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name "*.pyc" -exec rm -f {} +
	find . -name "*.log" -exec rm -f {} +
	docker system prune -f --volumes
	@echo "${GREEN}Limpieza completa.${NC}"