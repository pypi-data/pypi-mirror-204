import logging
from unittest import TestCase, main
from unittest import main as umain
from unittest.mock import PropertyMock, Mock, patch
from mcu import MCUResults

TEST_LOG = """
Disabling flash remapping function
Bootloader Version 1.9.0
Primary   slot: version=1.0.0+1001
Image 0 Secondary slot: Image not found
Found a candidate in slot 0
writing copy_done; fa_id=0 off=0x1fffe0 (0x23ffe0)
Image 0 loaded from the primary slot
Bootloader chainload address offset: 0x40000
Reset_Handler address offset: 0x40400
Jumping to the image
Booting the primary slot - flash remapping is disabled
hello sbl.
Disabling flash remapping function
Bootloader Version 1.9.0
Primary   slot: version=1.0.0+1001
Image 0 Secondary slot: Image not found
Image 0 loaded from the primary slot
Bootloader chainload address offset: 0x40000
Reset_Handler address offset: 0x40400
Jumping to the image
Booting the primary slot - flash remapping is disabled
Initializing PHY...
0 0 [Tmr Svc] AKNano vApplicationDaemonTaskStartupHook.
1 2000 [btn_read_task] [INFO] [36mButton state=1[0m
2 3331 [Tmr Svc] Getting IP address from DHCP ...
3 3443 [Tmr Svc] IPv4 Address: 192.168.0.134
4 3444 [Tmr Svc] DHCP OK
5 3446 [Tmr Svc] [INFO] SNTP started
6 4000 [btn_read_task] [INFO] [36mButton state=1[0m
7 4458 [tcpip_thread] [INFO] SNTP sntp_set_system_time
8 4459 [tcpip_thread] [INFO] SNTP time: 24.04.2023 09:58:02  sec=1682330282 boot_up_epoch=ld xTaskGetTickCount()=540028728
9 5946 [Tmr Svc] [INFO] Proceeding after sntp after waiting 0 seconds
10 5952 [iot_thread] [INFO ][DEMO][lu] ---------STARTING DEMO---------
ok: start string found, lava test monitoring started
test monitoring timeout: 600 seconds
11 5954 [iot_thread] [INFO ][INIT][lu] SDK successfully initialized.
12 5956 [iot_thread] [INFO ][DEMO][lu] Successfully initialized the demo. Network type for the demo: 4
13 5956 [iot_thread] [INFO] TEST aknano_init AKNANO_HASH=898628fcf74880279e32099bade6478ff4fb923b
14 5956 [iot_thread] [INFO] TEST aknano_init MANIFEST_HASH=7b2205c5c53623c19b35c926cd4400e4b99b0391
15 5958 [iot_thread] [INFO] [33mstart_aknano mode 'No Secure Element'[0m
16 5958 [iot_thread] [INFO] [33mProvisioning support is enabled[0m
17 5958 [iot_thread] [INFO] Initializing ak-nano...
18 5960 [iot_thread] [INFO] aknano_init_settings: serial=
19 5960 [iot_thread] [INFO] Device serial set? NO
20 5962 [iot_thread] [WARN] [31mDevice certificate (and/or serial) is not set. Running provisioning process[0m
21 5962 [iot_thread] [INFO] *CAAM Job Ring 0* :
22 5962 [iot_thread] [INFO] uuid=9829C3CE-B33D-66C4-7332-6E1C0E044D7C
23 5964 [iot_thread] [INFO] serial=9829C3CEB33D66C473326E1C0E044D7C
24 5964 [iot_thread] [INFO] aknano_gen_device_certificate_and_key
25 6000 [btn_read_task] [INFO] [36mButton state=1[0m
26 6619 [iot_thread] [INFO] aknano_gen_device_certificate_and_key key created
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIDeywg0bHrZvV0Zql4IYtFA1J01Y0Ve1Mc9adDKIXEW+oAoGCCqGSM49
AwEHoUQDQgAEvIhs6JZ7rGTyCvFKe1J9dCsrZC0LkQxEzvRv33YHDggxmtsm+0tv
eVK8Lx2/bOqGqsiPJa9CzwlZujEe7gjxoA==
-----END EC PRIVATE KEY-----
27 6660 [iot_thread] [INFO] aknano_gen_random_device_certificate_and_key ret=0
28 6660 [iot_thread] [INFO] cert_buf:
-----BEGIN CERTIFICATE-----
MIIBhDCCASmgAwIBAgIRAJgpw86zPWbEczJuHA4ETXwwDAYIKoZIzj0EAwIFADA8
MSUwIwYDVQQDDBxmaW8tNjEyNjNjODY0ZGUzNDM5NGVkOGI2NmU0MRMwEQYDVQQL
DApsbXAtY2ktbWN1MB4XDTIxMDEwMTAwMDAwMFoXDTMwMTIzMTIzNTk1OVowRDEt
MCsGA1UEAwwkOTgyOUMzQ0UtQjMzRC02NkM0LTczMzItNkUxQzBFMDQ0RDdDMRMw
EQYDVQQLDApsbXAtY2ktbWN1MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEvIhs
6JZ7rGTyCvFKe1J9dCsrZC0LkQxEzvRv33YHDggxmtsm+0tveVK8Lx2/bOqGqsiP
Ja9CzwlZujEe7gjxoKMCMAAwDAYIKoZIzj0EAwIFAANHADBEAiANBoa+Bl5nC6xu
D1FHtUipAmsM20CytQE2PvMjyBHvUAIgLz4qjp53c75bQhsqewrNdntYKHcWl67q
qnLxDvpcxj8=
-----END CERTIFICATE-----
29 6662 [iot_thread] [INFO] key_buf:
-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIDeywg0bHrZvV0Zql4IYtFA1J01Y0Ve1Mc9adDKIXEW+oAoGCCqGSM49
AwEHoUQDQgAEvIhs6JZ7rGTyCvFKe1J9dCsrZC0LkQxEzvRv33YHDggxmtsm+0tv
eVK8Lx2/bOqGqsiPJa9CzwlZujEe7gjxoA==
-----END EC PRIVATE KEY-----
30 6662 [iot_thread] [INFO] Clearing provisioned device data from flash
31 6713 [iot_thread] [INFO] Provisioning Key and Certificate using PKCS#11 interface. Using flash device
32 6719 [iot_thread] Write certificate...
33 6729 [iot_thread] [INFO] Provisioning done
34 8000 [btn_read_task] [INFO] [36mButton state=1[0m
35 10000 [btn_read_task] [INFO] [36mButton state=1[0m
36 12000 [btn_read_task] [INFO] [36mButton state=1[0m
37 12739 [iot_thread] [INFO] Device certificate available? YES
38 12739 [iot_thread] [INFO] Initializing settings...
39 12741 [iot_thread] [INFO] aknano_init_settings: image_position=1
40 12741 [iot_thread] [INFO] aknano_init_settings: aknano_settings->running_version=1001
41 12743 [iot_thread] [INFO] aknano_init_settings: serial=9829C3CEB33D66C473326E1C0E044D7C
42 12743 [iot_thread] [INFO] aknano_init_settings: uuid=9829C3CE-B33D-66C4-7332-6E1C0E044D7C
43 12743 [iot_thread] [INFO] aknano_init_settings: last_applied_version=0
44 12745 [iot_thread] [INFO] aknano_init_settings: last_confirmed_version=0
45 12745 [iot_thread] [INFO] aknano_init_settings: ongoing_update_correlation_id=
46 12747 [iot_thread] [INFO] aknano_init_settings: rollback_retry_count=0
47 12847 [iot_thread] [INFO] aknano_init_settings: rollback_next_retry_time=539837916
48 12847 [iot_thread] [INFO] aknano_init_settings: device_name=MIMXRT1170-EVK-9829C3CEB33D66C473326E1C0E044D7C
49 12949 [iot_thread] [INFO] aknano_init_settings: is_running_rolled_back_image=0
50 13049 [iot_thread] [INFO] TEST aknano_init UUID=9829C3CE-B33D-66C4-7332-6E1C0E044D7C
51 13049 [iot_thread] [INFO] TEST aknano_init RUNNING_VERSION=1001
52 13049 [iot_thread] [INFO] TEST aknano_init RUNNING_FROM_SLOT=1
53 13251 [iot_thread] [INFO] [32mCurrent image state is Permanent[0m
54 13255 [iot_thread] [INFO] MEMORY (Before aknano_checkin): Stack high watermark: 7598.  Minimum free heap: 144368
55 13255 [iot_thread] [INFO] aknano_checkin. Version=1001  Tag=devel
56 13980 [iot_thread] [INFO] Device has no config set
57 14000 [btn_read_task] [INFO] [36mButton state=1[0m
58 14248 [iot_thread] [INFO] fill_network_info: { \"local_ipv4\": \"192.168.0.134\", \"mac\": \"54:27:8d:4f:2c:8f\"}
59 14933 [iot_thread] [INFO] [35mtuf_client_fetch_file: 1.root.json HTTP operation return code 200. Body length=1447[0m
60 14933 [iot_thread] [INFO] aknano_provision_tuf_root: fetch_file  ret=805895636 file_size=0
61 14945 [iot_thread] [INFO] [35mtuf_client_write_local_file: role=root len=1447 OK[0m
62 15076 [iot_thread] [INFO] [35mtuf_client_fetch_file: 2.root.json HTTP operation return code 200. Body length=1640[0m
63 15154 [iot_thread] [INFO] [35mtuf_client_write_local_file: role=root len=1640 OK[0m
64 15273 [iot_thread] [INFO] [35mtuf_client_fetch_file: 3.root.json HTTP operation return code 404. Body length=18[0m
65 15275 [iot_thread] [INFO] [35mtuf_client_read_local_file: role=timestamp file not found. buf[0]=FF[0m
66 15392 [iot_thread] [INFO] [35mtuf_client_fetch_file: timestamp.json HTTP operation return code 404. Body length=18[0m
67 15393 [iot_thread] [INFO] [35mtuf_refresh TUF_HTTP_NOT_FOUND (-404)[0m
68 15404 [iot_thread] [INFO] MEMORY (After aknano_checkin): Stack high watermark: 4413.  Minimum free heap: 134904
69 15404 [iot_thread] [INFO] * Check-in failed with error -404
"""

logger = logging.getLogger()
logger.setLevel(logging.ERROR)


class MCUResultsPluginTest(TestCase):
    def setUp(self):
        self.plugin = MCUResults()

    def test_postprocess_testrun(self):
        testrun = Mock()
        testrun.log_file = TEST_LOG
        testrun.metadata = {
            "RUNNING_VERSION": "1001",
            "RUNNING_FROM_SLOT": "2",
            "NON_EXISTING_KEY": "value",
        }

        def goc_mock(*args, **kwargs):
            return kwargs, False

        def goc_suite(*args, **kwargs):
            return Mock(), False

        def goc_status(*args, **kwargs):
            return Mock(), False

        def goc_mock1(*args, **kwargs):
            return kwargs, False

        class KnownIssueMock:
            def __init__(self, title, test_name):
                self.environments = set()
                self.title = title
                self.test_name = test_name
                self.saved = False

            def save(self):
                self.saved = True

        def goc_knownissues_active(*args, **kwargs):
            return []

        with patch("squad.core.models.SuiteMetadata.objects.get_or_create", goc_mock1), \
            patch("squad.core.models.Suite.objects.get_or_create", goc_suite), \
            patch("squad.core.models.Test.objects.create", goc_mock), \
            patch("squad.core.models.Status.objects.filter", goc_status), \
            patch("squad.core.models.ProjectStatus.create_or_update", goc_mock), \
            patch("squad.core.tasks.RecordTestRunStatus", goc_mock), \
            patch("squad.core.models.KnownIssue.active_by_environment", goc_knownissues_active):
            self.plugin.postprocess_testrun(testrun)
            goc_mock1.assert_called()
            assert 2 == goc_mock1.call_count


if __name__ == "__main__":
    umain()
