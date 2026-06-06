import pytest
import os
import sys
import json

# Добавляем корень проекта в пути
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agent import AI_Agent
from src.utils import load_config, log_action

class Test_AI_Agent:
    def test_create_agent(self):
        agent = AI_Agent(name="TestBot", history_file="test_memory.json")
        assert agent.name == "TestBot"
        assert isinstance(agent.history, list)
        if os.path.exists("test_memory.json"):
            os.remove("test_memory.json")

    def test_add_message(self):
        agent = AI_Agent(name="TestBot", history_file="test_memory.json")
        agent.add_message("user", "Привет!")
        assert len(agent.history) == 1
        assert agent.history[0]["role"] == "user"
        if os.path.exists("test_memory.json"):
            os.remove("test_memory.json")

    def test_get_response(self):
        agent = AI_Agent(name="TestBot", history_file="test_memory.json")
        response = agent.get_response("Привет!")
        assert isinstance(response, str)
        assert len(response) > 0
        assert len(agent.history) == 2
        if os.path.exists("test_memory.json"):
            os.remove("test_memory.json")

    def test_history_persistence(self):
        agent1 = AI_Agent(name="TestBot", history_file="test_memory.json")
        agent1.add_message("user", "Test 1")
        agent1.add_message("assistant", "Ответ 1")

        agent2 = AI_Agent(name="TestBot", history_file="test_memory.json")
        assert len(agent2.history) == 2

        if os.path.exists("test_memory.json"):
            os.remove("test_memory.json")


class TestUtils:
    def test_load_config_creates_default(self):
        test_config = "test_config.json"
        if os.path.exists(test_config):
            os.remove(test_config)

        config = load_config(config_path=test_config)
        assert "bot_name" in config
        assert "log_file" in config
        assert "history_file" in config
        assert os.path.exists(test_config)
        os.remove(test_config)

    def test_load_config_reads_existing(self):
        test_config = "test_config.json"
        custom_config = {
            "bot_name": "CustomBot",
            "log_file": "custom.log",
            "history_file": "custom.json"
        }

        with open(test_config, "w", encoding="utf-8") as f:
            json.dump(custom_config, f)

        config = load_config(config_path=test_config)
        assert config["bot_name"] == "CustomBot"
        os.remove(test_config)

    def test_log_action_creates_file(self):
        test_log = "test.log"
        if os.path.exists(test_log):
            os.remove(test_log)

        log_action("Тестовое сообщение", log_file=test_log)
        assert os.path.exists(test_log)

        with open(test_log, "r", encoding="utf-8") as f:
            content = f.read()
            assert "Тестовое сообщение" in content

        os.remove(test_log)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])