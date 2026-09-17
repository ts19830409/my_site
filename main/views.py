from django.contrib import messages
from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .models import Award, Certificate, Message, Project


def favicon(request):
    path = finders.find("img/favicon.ico")
    if not path:
        raise Http404("favicon not found")
    response = FileResponse(open(path, "rb"), content_type="image/x-icon")
    response["Cache-Control"] = "public, max-age=604800"
    return response


def index(request):
    return render(request, "main/index.html")


def projects(request):
    projects = Project.objects.all()
    return render(request, "main/projects.html", {"projects": projects})


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "main/project_detail.html", {"project": project})


def certificates(request):
    certificates = Certificate.objects.filter(is_archived=False)
    return render(request, "main/certificates.html", {"certificates": certificates})


def certificates_archive(request):
    archived_certificates = Certificate.objects.filter(is_archived=True)
    return render(
        request,
        "main/certificates_archive.html",
        {"archived_certificates": archived_certificates},
    )


def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        text = request.POST.get("text", "").strip()

        if name and email and text:
            Message.objects.create(name=name, email=email, text=text)

            try:
                recipient = settings.EMAIL_HOST_USER
                if recipient:
                    mail = EmailMessage(
                        subject=f"Новое сообщение от {name}",
                        body=f"Имя: {name}\nEmail: {email}\n\n{text}",
                        to=[recipient],
                    )
                    mail.send()
            except Exception:
                pass

            messages.success(request, "Сообщение отправлено! Спасибо.")
            return redirect("main:contacts")

        messages.error(request, "Заполните все поля")

    return render(request, "main/contacts.html")


def awards(request):
    awards = Award.objects.all()
    return render(request, "main/awards.html", {"awards": awards})


def lab(request):
    nodes = [
        {
            "name": "ws-001",
            "label": "ws-001 (Ubuntu 26.04)",
            "icon": "pc",
            "role": "рабочая станция",
            "os": "Intel Core i3-2120",
            "po": "- VSCode\n- Chromium\n- Remmina\n- Python\n- Libre Office\n- Midnight Commander",
            "disks": [
                ("ssd 120 Гб — система", ""),
                ("hdd 250 Гб — документы и проекты", ""),
            ],
            "x": 110, "y": 230,
        },
        {
            "name": "ws-002",
            "label": "ws-002 (Windows 10)",
            "icon": "pc",
            "role": "рабочая станция",
            "os": "Intel Core i3-540",
            "po": "- Delphi\n- FineReader\n- MSOffice\n- pgAdmin4\n- Photoshop",
            "disks": [
                ("hdd 160 Гб — система", ""),
                ("hdd 500 Гб — документы", ""),
                ("hdd 1 Тб × 3 — видео", ""),
            ],
            "x": 110, "y": 370,
        },
        {
            "name": "nb-001",
            "label": "nb-001 (Linux Mint 22.3)",
            "icon": "laptop",
            "role": "ноутбук",
            "os": "Celeron N4100",
            "po": "- VSCode\n- Chromium\n- Remmina\n- Python\n- Libre Office\n- Midnight Commander",
            "disks": [("ssd 120 — система и документы", "")],
            "x": 295, "y": 420,
        },
        {
            "name": "srv-001",
            "label": "srv-001 (Ubuntu 24.04)",
            "icon": "server",
            "role": "сервер инфраструктуры",
            "os": "Pentium E2220",
            "po": "- samba\n- Docker\n- Gitea\n- PostgreSQL\n- Redis\n- libvirt",
            "disks": [
                ("hdd 250 Гб — ОС + приложения", ""),
                ("hdd 500 Гб — сетевое хранилище", ""),
                ("hdd 120 Гб — бэкапы", ""),
                ("ssd 120 Гб — образы VM", ""),
            ],
            "x": 480, "y": 230,
        },
        {
            "name": "srv-002",
            "label": "srv-002 (Debian 11.7)",
            "icon": "server",
            "role": "тестовый deploy",
            "os": "QEMU",
            "po": "- Docker\n- Compose\n- Nginx",
            "disks": [
                ("vda 20 Гб — система", ""),
            ],
            "x": 480, "y": 370,
        },
        {
            "name": "vps-001",
            "icon": "cloud",
            "role": "арендованный VPS",
            "x": 190, "y": 100,
        },
        {
            "name": "vps-002",
            "icon": "cloud",
            "role": "арендованный VPS",
            "x": 400, "y": 100,
        },
        {
            "name": "router",
            "icon": "router",
            "role": "Wi-Fi роутер TP-Link Archer C6U",
            "x": 295, "y": 270,
        },
    ]
    nodes.sort(key=lambda n: n["x"], reverse=True)

    edge_pairs = [
        ("router", "ws-001"),
        ("router", "ws-002"),
        ("router", "srv-001"),
        ("router", "nb-001"),
        ("srv-001", "srv-002"),
        ("router", "vps-002"),
        ("router", "vps-001"),
    ]

    wg_pairs = [
        ("vps-002", "ws-001"),
        ("vps-002", "nb-001"),
        ("vps-001", "ws-001"),
        ("vps-001", "nb-001"),
    ]

    internet_pairs = {
        ("router", "vps-002"),
        ("router", "vps-001"),
    }

    pos = {n["name"]: (n["x"], n["y"]) for n in nodes}

    edges = []
    for a, b in edge_pairs:
        edges.append({
            "a": a, "b": b,
            "x1": pos[a][0], "y1": pos[a][1],
            "x2": pos[b][0], "y2": pos[b][1],
            "wg": False,
            "internet": (a, b) in internet_pairs,
        })
    for a, b in wg_pairs:
        edges.append({
            "a": a, "b": b,
            "x1": pos[a][0], "y1": pos[a][1],
            "x2": pos[b][0], "y2": pos[b][1],
            "wg": True,
        })

    return render(request, "main/lab.html", {"nodes": nodes, "edges": edges})
