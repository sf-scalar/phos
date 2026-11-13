import setup


def test_nvidia_smi_uses_absolute_known_path(monkeypatch):
    calls = []

    monkeypatch.setattr(setup.platform, "system", lambda: "Linux")
    monkeypatch.setattr(setup.shutil, "disk_usage", lambda _: (0, 0, 0))
    monkeypatch.setattr(
        setup.os.path, "isfile", lambda path: path == "/usr/bin/nvidia-smi"
    )
    monkeypatch.setattr(
        setup.shutil,
        "which",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("PATH lookup must not be used")
        ),
    )

    def check_output(args, **_kwargs):
        calls.append(args)
        return "Test GPU, 8192\n"

    monkeypatch.setattr(setup.subprocess, "check_output", check_output)

    specs = setup.get_system_specs()

    assert specs["has_nvidia"]
    assert calls[0][0] == "/usr/bin/nvidia-smi"
