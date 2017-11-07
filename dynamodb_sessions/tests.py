from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
from dynamodb_sessions.backends.dynamodb import (
    SessionStore, dynamodb_connection_factory,
    TABLE_NAME
)
from botocore.exceptions import ClientError


class DynamoDbTestCase(TestCase):

    def setUp(self):
        call_command('create_session_table')

    def tearDown(self):
        connection = dynamodb_connection_factory(lowlevel=True)
        connection.delete_table(
            TableName=TABLE_NAME
        )

    def test_with_user_generated_session_key(self):
        session_key = "12345678"
        session = SessionStore(session_key=session_key)
        session._session.keys()
        session._session_key = session_key
        session.save(must_create=True)
        session['name'] = 'test'
        session.save()
        new_session = SessionStore(session_key=session_key)
        self.assertEqual(
            new_session['name'],
            'test'
        )

    def test_creating_session_with_empty_session_key(self):
        session = SessionStore()
        session['name'] = 'test'
        session.save()

        self.assertEqual(
            SessionStore(session_key=session.session_key)['name'],
            'test'
        )


class TestManagementCommands(TestCase):

    def setUp(self):
        connection = dynamodb_connection_factory(lowlevel=True)
        try:
            connection.delete_table(
                TableName=TABLE_NAME
            )
        except ClientError as e:
            if e.response['Error']['Code'] != \
                    'ResourceNotFoundException':
                raise e

    def test_command_output(self):
        out = StringIO()
        call_command('create_session_table', stdout=out)
        self.assertEqual("session table created\n", out.getvalue())

        # check table was created
        connection = dynamodb_connection_factory(lowlevel=True)
        connection.describe_table(TableName=TABLE_NAME)

        # calling for the second time
        out = StringIO()
        call_command('create_session_table', stdout=out)
        self.assertEqual("session table already exist\n", out.getvalue())
