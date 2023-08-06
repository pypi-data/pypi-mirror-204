import time
import uuid
from datetime import datetime, timedelta

from tqdm.auto import tqdm

from chalk._reporting.models import BatchOpStatus
from chalk.client import ChalkOfflineQueryException
from chalk.client.exc import ChalkGetBatchReportException


class ProgressService:
    def __init__(self, operation_id: uuid.UUID, client: "ChalkAPIClientImpl"):
        self.operation_id = operation_id
        self.client = client

    def show_progress_bars(self):
        fqn_to_pbar = {}
        poll_interval = 2
        main_pbar = None
        timeout = datetime.now() + timedelta(hours=3)
        first_missing_report_dt = None

        while datetime.now() < timeout:
            time.sleep(poll_interval)

            batch_report = self.client._get_batch_report(self.operation_id)
            if batch_report is None:
                first_missing_report_dt = first_missing_report_dt or datetime.now()
                if datetime.now() > first_missing_report_dt + timedelta(minutes=1):
                    raise TimeoutError("Timed out waiting for status report of operation")
                else:
                    continue
            else:
                first_missing_report_dt = None

            num_resolvers = len(batch_report.resolvers)
            if (
                num_resolvers == 0
                and main_pbar is None
                and batch_report.status not in [BatchOpStatus.COMPLETED, BatchOpStatus.FAILED]
            ):
                # Displaying a progress bar with 0 total shows up odd initially,
                # and can't be fixed by updating the total later.
                continue

            # Placement of the main progress bar updating block matters.
            # If we're starting out, update the main progress bar before updating the resolver progress bars
            if main_pbar is None:
                main_pbar = tqdm(total=num_resolvers, desc="Resolvers executed", position=0, leave=True)

            # Create pbar if new resolvers have been added
            for resolver_report in batch_report.resolvers:
                fqn = resolver_report.resolver_fqn
                if fqn not in fqn_to_pbar:
                    short_name = fqn.split(".")[-1]
                    fqn_to_pbar[fqn] = tqdm(
                        total=resolver_report.progress.total or 1,  # Avoid 0 total
                        desc=f"[ {short_name} ] rows",
                        position=1,
                        leave=True,
                    )

            for resolver_report in batch_report.resolvers:
                fqn = resolver_report.resolver_fqn
                resolver_pbar = fqn_to_pbar[fqn]

                if resolver_report.progress.total == 0 and resolver_pbar.n == 0:
                    resolver_pbar.n = 1
                    resolver_pbar.close()
                else:
                    rows_done = resolver_report.progress.computed + resolver_report.progress.failed
                    if resolver_report.progress.computed != resolver_pbar.n:
                        resolver_pbar.n = resolver_report.progress.computed
                        resolver_pbar.refresh()
                        if rows_done == resolver_pbar.total:
                            resolver_pbar.close()

            # Placement of the main progress bar updating block matters.
            # If we're in progress, update the resolvers (above) before updating the main progress bar
            changed = False
            if batch_report.progress.total != main_pbar.total:
                main_pbar.total = batch_report.progress.total
                changed = True

            if batch_report.progress.computed != main_pbar.n:
                main_pbar.n = batch_report.progress.computed
                changed = True

            if changed:
                main_pbar.refresh()

            if batch_report.status == BatchOpStatus.COMPLETED:
                main_pbar.set_description(main_pbar.desc + " ■ ")
                main_pbar.close()
                break

            if batch_report.status == BatchOpStatus.FAILED:
                main_pbar.set_description(main_pbar.desc + " ✗ ")

                if batch_report.error is not None:
                    main_pbar.set_postfix(error=batch_report.error.message)
                main_pbar.close()

                if batch_report.error is not None:
                    raise ChalkOfflineQueryException(errors=[batch_report.error])

                break

        else:
            raise TimeoutError("Timed out waiting for operation to finish")
