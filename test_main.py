from fastapi.testclient import TestClient
from main import app
from uuid import uuid4

client = TestClient(app)


# Teste 1: acesso a API sem uma rota ('/')
def test_read_main_returns_not_found():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


# Teste 2: criar uma task qualquer e em seguida deletar esta task
def test_create_task_and_delete_it():
    response = client.post(
        "/task", json={"description": "task qualquer", "completed": "False"}
    )
    assert response.status_code == 200

    response2 = client.delete(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == None  # Serve para evitar conflitos no futuro


# Teste 3: deletar uma task que não existe
def test_delete_nonexistent_task():
    # Cria um UUID aleatório para depois tentar apagar a task com este UUID
    inv_uuid = uuid4()

    response = client.delete(f"/task/{inv_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


# Teste 4: get de uma task que existe
def test_get_existent_task():
    # Cria uma task nova qualquer
    response = client.post(
        "/task", json={"description": "task qualquer", "completed": "False"}
    )
    assert response.status_code == 200

    # Faz o get dessa task
    response2 = client.get(f"/task/{response.json()}")
    assert response2.status_code == 200
    assert response2.json() == {"description": "task qualquer", "completed": False}

    # Delete da task para evitar conflitos nos outros testes e manter a base de dados limpa
    response3 = client.delete(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == None


# Teste 5: get de uma task que não existe
def test_get_nonexistent_task():
    # Mesmo processo do teste 3, só que com get ao invés de delete
    inv_uuid = uuid4()

    response = client.get(f"/task/{inv_uuid}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


# Teste 6: rota '/task' retorna lista vazia quando a lista de tasks está vazia (acontece no acesso inicial a API)
def test_get_empty_list():
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {}


# Teste 7: rota '/task' retorna a lista completa de tasks quando ela não está vazia
def test_get_whole_list():
    # Criando três tasks quaisquer para encher a lista
    response1 = client.post(
        "/task", json={"description": "Aprender a criar testes", "completed": "True"}
    )
    assert response1.status_code == 200

    response2 = client.post(
        "/task",
        json={
            "description": "Rodar os testes e ver se tudo funciona",
            "completed": "True",
        },
    )
    assert response2.status_code == 200

    response3 = client.post(
        "/task",
        json={
            "description": "Descrições criativas para as tasks",
            "completed": "False",
        },
    )
    assert response3.status_code == 200

    # Get das tasks
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == {
        response1.json(): {
            "description": "Aprender a criar testes",
            "completed": True,
        },
        response2.json(): {
            "description": "Rodar os testes e ver se tudo funciona",
            "completed": True,
        },
        response3.json(): {
            "description": "Descrições criativas para as tasks",
            "completed": False,
        },
    }

    # Delete das tasks para evitar conflitos nos outros testes e manter a base de dados limpa
    d1 = client.delete(f"/task/{response1.json()}")
    assert d1.status_code == 200
    assert d1.json() == None

    d2 = client.delete(f"/task/{response2.json()}")
    assert d2.status_code == 200
    assert d2.json() == None

    d3 = client.delete(f"/task/{response3.json()}")
    assert d3.status_code == 200
    assert d3.json() == None


# Teste 8: achar tasks que estão completas
def test_get_completed_tasks():
    response1 = client.post(
        "/task", json={"description": "Aprender a criar testes", "completed": "True"}
    )
    assert response1.status_code == 200

    response2 = client.post(
        "/task",
        json={
            "description": "Rodar os testes e ver se tudo funciona",
            "completed": "True",
        },
    )
    assert response2.status_code == 200

    response3 = client.post(
        "/task",
        json={
            "description": "Descrições criativas para as tasks",
            "completed": "False",
        },
    )
    assert response3.status_code == 200

    # Get das tasks que estão completas
    response = client.get("/task?completed=true")
    assert response.status_code == 200
    assert response.json() == {
        response1.json(): {
            "description": "Aprender a criar testes",
            "completed": True,
        },
        response2.json(): {
            "description": "Rodar os testes e ver se tudo funciona",
            "completed": True,
        },
    }

    d1 = client.delete(f"/task/{response1.json()}")
    assert d1.status_code == 200
    assert d1.json() == None

    d2 = client.delete(f"/task/{response2.json()}")
    assert d2.status_code == 200
    assert d2.json() == None

    d3 = client.delete(f"/task/{response3.json()}")
    assert d3.status_code == 200
    assert d3.json() == None


# Teste 9: achar tasks que estão incompletas
def test_get_incomplete_tasks():
    response1 = client.post(
        "/task", json={"description": "Aprender a criar testes", "completed": "True"}
    )
    assert response1.status_code == 200

    response2 = client.post(
        "/task",
        json={
            "description": "Rodar os testes e ver se tudo funciona",
            "completed": "True",
        },
    )
    assert response2.status_code == 200

    response3 = client.post(
        "/task",
        json={
            "description": "Descrições criativas para as tasks",
            "completed": "False",
        },
    )
    assert response3.status_code == 200

    # Get das tasks que estão incompletas
    response = client.get("/task?completed=false")
    assert response.status_code == 200
    assert response.json() == {
        response3.json(): {
            "description": "Descrições criativas para as tasks",
            "completed": False,
        },
    }

    d1 = client.delete(f"/task/{response1.json()}")
    assert d1.status_code == 200
    assert d1.json() == None

    d2 = client.delete(f"/task/{response2.json()}")
    assert d2.status_code == 200
    assert d2.json() == None

    d3 = client.delete(f"/task/{response3.json()}")
    assert d3.status_code == 200
    assert d3.json() == None


# Teste 10: atualizar uma task que existe usando patch
def test_patch_existent_task():
    response = client.post(
        "/task", json={"description": "task qualquer", "completed": "False"}
    )
    assert response.status_code == 200

    response2 = client.patch(
        f"/task/{response.json()}",
        json={"description": "visitar https://theuselessweb.com/", "completed": "True"},
    )
    assert response2.status_code == 200
    assert response2.json() == None

    # Checa se o patch deu certo
    response3 = client.get(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == {
        "description": "visitar https://theuselessweb.com/",
        "completed": True,
    }

    response4 = client.delete(f"/task/{response.json()}")
    assert response4.status_code == 200
    assert response4.json() == None


# Teste 11: atualizar uma task que não existe usando patch
def test_patch_nonexistent_task():
    inv_uuid = uuid4()
    print(inv_uuid)
    response = client.patch(
        f"/task/{inv_uuid}",
        json={"description": "esta task não existe", "completed": "False"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


# Teste 12: atualizar uma task que existe usando put
def test_put_existent_task():
    response = client.post(
        "/task", json={"description": "task qualquer", "completed": "False"}
    )
    assert response.status_code == 200

    response2 = client.put(
        f"/task/{response.json()}",
        json={"description": "outra task qualquer", "completed": "True"},
    )
    assert response2.status_code == 200
    assert response2.json() == None

    # Checa se o put deu certo
    response3 = client.get(f"/task/{response.json()}")
    assert response3.status_code == 200
    assert response3.json() == {
        "description": "outra task qualquer",
        "completed": True,
    }

    response4 = client.delete(f"/task/{response.json()}")
    assert response4.status_code == 200
    assert response4.json() == None


# Teste 13: usar put passando uma string qualquer como UUID
def test_put_invalid_uuid():
    inv_uuid = "Isto não é um UUID"
    response = client.put(
        f"/task/{inv_uuid}",
        json={"description": "task com id string", "completed": "False"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "uuid_"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid",
            }
        ]
    }


# Teste 14: usar patch passando uma string qualquer como UUID
def test_patch_invalid_uuid():
    inv_uuid = "Isto não é um UUID"
    response = client.patch(
        f"/task/{inv_uuid}",
        json={"description": "task com id string", "completed": "False"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "uuid_"],
                "msg": "value is not a valid uuid",
                "type": "type_error.uuid",
            }
        ]
    }
