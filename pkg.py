import csv
from json import dumps
from enum import Enum

class Activity(Enum):
	INBOUND_CALL = 'Inbound Call'
	HANDLE_CASE = 'Handle Case'
	CALL_OUTBOUND = 'Call Outbound'
	INBOUND_EMAIL = 'Inbound Email'
	EMAIL_OUTBOUND = 'Email Outbound'
	HANDLE_EMAIL = 'Handle Email'


SERVED_CASE: list[str] = [
	Activity.CALL_OUTBOUND.value,
	Activity.EMAIL_OUTBOUND.value,
	Activity.HANDLE_EMAIL.value,
	Activity.HANDLE_CASE.value
]


class Log:
	def __init__(
		self,
		case_id: int,
		activity: str,
		start_date: str,
		end_date: str,
		agent_position: str,
		customer_id: int,
		product: str,
		service_type: str,
		resource: str,
	) -> None:
		self.case_id: int = case_id
		self.activity: str = activity
		self.start_date: str = start_date
		self.end_date: str = end_date
		self.agent_position: str = agent_position
		self.customer_id: str = customer_id
		self.product: str = product
		self.service_type: str = service_type
		self.resource: str = resource


class Case:
	def __init__(
		self,
		id: int,
		last_activity: str,
		logs: list[Log],
		steps: int,
	) -> None:
		self.id: int = id
		self.last_activity: str = last_activity
		self.logs: list[Log] = logs
		self.steps: int = steps
		self.served: bool = self.__is_served()

	def __is_served(self) -> bool:
		for log in self.logs:
			if log.activity in SERVED_CASE:
				return True

		return False
	
	def to_json(self):
		aux_logs = []

		for log in self.logs:
			aux_logs.append(
				log.__dict__
			)

		return dumps(
			{
				'id': self.id,
				'last_activity': self.last_activity,
				'steps': self.steps,
				'served': self.served,
				'logs': aux_logs.copy(),
			},
			indent=3,
		)


def get_logs(file_path: str) -> list[Log]:
	logs: list[Log] = []

	with open(file_path, 'r') as file:
		csv_reader = csv.reader(file)
		next(csv_reader)

		for row in csv_reader:
			new_log: Log = Log(
				int(row[0].split(' ')[1]), # Case ID
				row[1], # Activity
				row[2], # Start Date
				row[3], # End Date
				row[4], # Agent Position
				row[5], # Customer ID
				row[6], # Product
				row[7], # Service Type
				row[8], # Resource
			)

			logs.append(new_log)
	
	return logs


def get_cases(logs: list[Log]) -> list[Case]:
	cases: list[Case] = []

	current_case_id = logs[0].case_id
	aux_logs: list[list[Log]] = []
	aux_last_activity: str = ''

	for log in logs:
		# If same case id, save auxiliary info
		if( current_case_id == log.case_id ):
			current_case_id = log.case_id
			aux_last_activity = log.activity
			aux_logs.append(log)
			continue
		
		case = Case(
			current_case_id,
			aux_last_activity,
			aux_logs.copy(),
			len(aux_logs)
		)

		cases.append(case)

		current_case_id = log.case_id
		aux_logs.clear()
		aux_logs.append( log )
		aux_last_activity = log.activity
	
	return cases


def get_header(file_path: str) -> list[str]:
	header = []
	with open(file_path, 'r') as file:
		csv_reader = csv.reader(file)

		header = next(csv_reader).copy()
	
	return header
