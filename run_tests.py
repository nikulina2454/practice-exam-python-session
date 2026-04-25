#!/usr/bin/env python3
"""
Скрипт для запуска автотестов
Используется для проверки выполнения заданий
"""

import sys
import os
import subprocess


def run_tests():
    """Запуск всех тестов"""
    print("=" * 60)
    print("ЗАПУСК АВТОТЕСТОВ ДЛЯ ПРОВЕРКИ ЗАДАНИЙ")
    print("=" * 60)

    # Проверяем наличие pytest
    try:
        import pytest

        print("[OK] pytest найден")
    except ImportError:
        print("[ERROR] pytest не найден. Установите: pip install pytest")
        return False

    # Список тестовых файлов
    test_files = [
        "tests/test_user.py",
        "tests/test_project.py",
        "tests/test_task.py",
    ]

    # Проверяем наличие тестовых файлов
    missing_files = []
    for test_file in test_files:
        if not os.path.exists(test_file):
            missing_files.append(test_file)

    if missing_files:
        print("[ERROR] Отсутствуют тестовые файлы:")
        for file in missing_files:
            print(f"  - {file}")
        return False

    print("[OK] Все тестовые файлы найдены")

    # Запускаем тесты
    print("\n" + "=" * 60)
    print("ЗАПУСК ТЕСТОВ МОДЕЛЕЙ")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_project.py", "-v"],
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)

    except Exception as e:
        print(f"Ошибка запуска тестов моделей: {e}")

    print("\n" + "=" * 60)
    print("ЗАПУСК ТЕСТОВ КОНТРОЛЛЕРОВ")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_task.py", "-v"],
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)

    except Exception as e:
        print(f"Ошибка запуска тестов: {e}")

    print("\n" + "=" * 60)
    print("ЗАПУСК ТЕСТОВ БАЗЫ ДАННЫХ")
    print("=" * 60)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/test_user.py", "-v"],
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)

    except Exception as e:
        print(f"Ошибка запуска тестов: {e}")

    print("\n" + "=" * 60)
    print("ПОВТОРНЫЙ ЗАПУСК ВСЕХ ТЕСТОВ")
    print("=" * 60)

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/",
                "-v",
            ],
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print("Ошибки:", result.stderr)

    except Exception as e:
        print(f"Ошибка запуска тестов с покрытием: {e}")

    print("\n" + "=" * 60)
    print("ИНСТРУКЦИИ ПО ЗАПУСКУ")
    print("=" * 60)
    print("Для запуска всех тестов: pytest -v")
    print("Для запуска всех тестов в тихом режиме: pytest -q")
    print("Для запуска конкретных тестов:")
    print("  pytest -v tests/test_user.py")
    print("  pytest -v tests/test_project.py")
    print("  pytest -v tests/test_task.py")

    return True


if __name__ == "__main__":
    run_tests()
