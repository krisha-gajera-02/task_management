import argparse
import json
import os
import sys
import logging
from datetime import datetime

DATA_FILE = "data/tasks.json"
LOG_FILE = "app.log"

os.makedirs("data", exist_ok=True)

# ------------------ Logging Setup ------------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ Utility Functions ------------------
def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        content = f.read().strip()
        return json.loads(content) if content else []


def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def get_next_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1


def print_task(task):
    print("-" * 50)
    for key, value in task.items():
        print(f"{key.capitalize():15}: {value}")
    print("-" * 50)


# ------------------ CLI Logic ------------------
def main():
    parser = argparse.ArgumentParser(
        description="CLI Based Task Management System",
        allow_abbrev=False
    )

    subparsers = parser.add_subparsers(dest="command")

    # -------- ADD --------
    add = subparsers.add_parser(
        "add", help="Add a new task", allow_abbrev=False
    )
    add.add_argument("--title", nargs="+")
    add.add_argument("--description", nargs="+")
    add.add_argument("--priority")

    # -------- LIST --------
    subparsers.add_parser(
        "list", help="View all tasks", allow_abbrev=False
    )

    # -------- VIEW --------
    view = subparsers.add_parser(
        "view", help="View task by ID", allow_abbrev=False
    )
    view.add_argument("--id", type=int, required=True)

    # -------- UPDATE --------
    update = subparsers.add_parser(
        "update", help="Update a task", allow_abbrev=False
    )
    update.add_argument("--id", type=int, required=True)
    update.add_argument("--title", nargs="+")
    update.add_argument("--description", nargs="+")
    update.add_argument("--priority")
    update.add_argument("--status")

    # -------- COMPLETE --------
    complete = subparsers.add_parser(
        "complete", help="Mark task as completed", allow_abbrev=False
    )
    complete.add_argument("--id", type=int, required=True)

    # -------- DELETE --------
    delete = subparsers.add_parser(
        "delete", help="Delete a task", allow_abbrev=False
    )
    delete.add_argument("--id", type=int, required=True)

    args, unknown = parser.parse_known_args()

    # -------- Unknown Argument Handling --------
    if unknown:
        print(f"❌ Invalid argument(s): {' '.join(unknown)}")
        print("Use --help to see valid options.")
        sys.exit(1)

    if not args.command:
        print("❌ Invalid command.")
        print("Use: add | list | view | update | complete | delete")
        sys.exit(1)

    tasks = load_tasks()

    # -------- ADD --------
    if args.command == "add":
        forbidden = {"--id", "--status", "--created_at", "--created-at"}

        for arg in sys.argv:
            if arg in forbidden:
                print(f"❌ {arg} will be provided by the system.")
                return

        missing = []
        if not args.title:
            missing.append("--title")
        if not args.description:
            missing.append("--description")
        if not args.priority:
            missing.append("--priority")

        if missing:
            for m in missing:
                print(f"❌ The {m} field is required.")
            return

        priority = args.priority.lower()
        if priority not in {"low", "medium", "high"}:
            print("❌ Priority must be low, medium, or high.")
            return

        task = {
            "id": get_next_id(tasks),
            "title": " ".join(args.title),
            "description": " ".join(args.description),
            "priority": priority,
            "status": "pending",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        tasks.append(task)
        save_tasks(tasks)
        logging.info(f"Task created: {task['id']}")
        print("✅ Task added successfully.")

    # -------- LIST --------
    elif args.command == "list":
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            print_task(task)

    # -------- VIEW --------
    elif args.command == "view":
        task = next((t for t in tasks if t["id"] == args.id), None)
        if not task:
            print("❌ Task not found.")
            return
        print_task(task)

    # -------- UPDATE --------
    elif args.command == "update":
        task = next((t for t in tasks if t["id"] == args.id), None)
        if not task:
            print("❌ Task not found.")
            return

        if not any([args.title, args.description, args.priority, args.status]):
            print("❌ No fields provided to update.")
            return

        if args.title:
            task["title"] = " ".join(args.title)

        if args.description:
            task["description"] = " ".join(args.description)

        if args.priority:
            p = args.priority.lower()
            if p not in {"low", "medium", "high"}:
                print("❌ Priority must be low, medium, or high.")
                return
            task["priority"] = p

        if args.status:
            s = args.status.lower()
            if s not in {"pending", "completed"}:
                print("❌ Status must be pending or completed.")
                return
            task["status"] = s

        save_tasks(tasks)
        logging.info(f"Task updated: {args.id}")
        print("✅ Task updated successfully.")

    # -------- COMPLETE --------
    elif args.command == "complete":
        task = next((t for t in tasks if t["id"] == args.id), None)
        if not task:
            print("❌ Task not found.")
            return
        task["status"] = "completed"
        save_tasks(tasks)
        logging.info(f"Task completed: {args.id}")
        print("✅ Task marked as completed.")

    # -------- DELETE --------
    elif args.command == "delete":
        task = next((t for t in tasks if t["id"] == args.id), None)
        if not task:
            print("❌ Task not found.")
            return
        tasks.remove(task)
        save_tasks(tasks)
        logging.info(f"Task deleted: {args.id}")
        print("✅ Task deleted successfully.")


if __name__ == "__main__":
    main()
