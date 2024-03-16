from pkg import Log, Case, get_logs, get_cases, get_header
import csv


FILE_PATH: str = 'ExampleLog.csv'


header: list[str] = get_header(FILE_PATH)
logs: list[Log] = get_logs(FILE_PATH)


cases: list[Case] = get_cases(logs)


# Save served cases in a file
with open('out/served.csv', 'w', newline='') as file:
	csv_writer = csv.writer(file)
	csv_writer.writerow(header)

	for case in cases:
		if(not case.served):
			continue

		for log in case.logs:
			csv_writer.writerow([
				f'Case {log.case_id}',
				log.activity,
				log.start_date,
				log.end_date,
				log.agent_position,
				log.agent_position,
				log.customer_id,
				log.product,
				log.service_type,
				log.resource
			])


# Save not served cases in a file
with open('out/not_served.csv', 'w', newline='') as file:
	csv_writer = csv.writer(file)
	csv_writer.writerow(header)

	for case in cases:
		if(case.served):
			continue

		for log in case.logs:
			csv_writer.writerow([
				f'Case {log.case_id}',
				log.activity,
				log.start_date,
				log.end_date,
				log.agent_position,
				log.agent_position,
				log.customer_id,
				log.product,
				log.service_type,
				log.resource
			])
