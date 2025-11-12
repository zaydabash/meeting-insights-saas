"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Organizations
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('domain', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_organizations_id'), 'organizations', ['id'], unique=False)
    op.create_index(op.f('ix_organizations_name'), 'organizations', ['name'], unique=False)
    op.create_index(op.f('ix_organizations_domain'), 'organizations', ['domain'], unique=False)

    # Users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.Enum('ADMIN', 'MEMBER', name='userrole'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_org_id'), 'users', ['org_id'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # Meetings
    op.create_table(
        'meetings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.Integer(), nullable=False),
        sa.Column('calendar_event_id', sa.String(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('occurred_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('duration_sec', sa.Float(), nullable=True),
        sa.Column('audio_url', sa.String(), nullable=True),
        sa.Column('transcript_text', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'PROCESSED', 'FAILED', name='meetingstatus'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_meetings_id'), 'meetings', ['id'], unique=False)
    op.create_index(op.f('ix_meetings_org_id'), 'meetings', ['org_id'], unique=False)
    op.create_index(op.f('ix_meetings_occurred_at'), 'meetings', ['occurred_at'], unique=False)
    op.create_index(op.f('ix_meetings_status'), 'meetings', ['status'], unique=False)
    op.create_index(op.f('ix_meetings_calendar_event_id'), 'meetings', ['calendar_event_id'], unique=False)

    # Speakers
    op.create_table(
        'speakers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meeting_id', sa.Integer(), nullable=False),
        sa.Column('label', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_speakers_id'), 'speakers', ['id'], unique=False)
    op.create_index(op.f('ix_speakers_meeting_id'), 'speakers', ['meeting_id'], unique=False)

    # Utterances
    op.create_table(
        'utterances',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meeting_id', sa.Integer(), nullable=False),
        sa.Column('speaker_id', sa.Integer(), nullable=False),
        sa.Column('start_ms', sa.Float(), nullable=False),
        sa.Column('end_ms', sa.Float(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
        sa.ForeignKeyConstraint(['speaker_id'], ['speakers.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_utterances_id'), 'utterances', ['id'], unique=False)
    op.create_index(op.f('ix_utterances_meeting_id'), 'utterances', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_utterances_speaker_id'), 'utterances', ['speaker_id'], unique=False)

    # Insights
    op.create_table(
        'insights',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('meeting_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.Enum('ACTION_ITEM', 'DECISION', 'SENTIMENT', 'SUMMARY', 'NOTE', name='insighttype'), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('owner_user_id', sa.Integer(), nullable=True),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('extra', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
        sa.ForeignKeyConstraint(['owner_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_insights_id'), 'insights', ['id'], unique=False)
    op.create_index(op.f('ix_insights_meeting_id'), 'insights', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_insights_type'), 'insights', ['type'], unique=False)
    op.create_index(op.f('ix_insights_owner_user_id'), 'insights', ['owner_user_id'], unique=False)

    # Tasks
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.Integer(), nullable=False),
        sa.Column('meeting_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('owner_user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('OPEN', 'IN_PROGRESS', 'DONE', name='taskstatus'), nullable=False),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('source', sa.Enum('INTERNAL', 'SLACK', 'JIRA', name='tasksource'), nullable=False),
        sa.Column('external_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
        sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
        sa.ForeignKeyConstraint(['owner_user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tasks_id'), 'tasks', ['id'], unique=False)
    op.create_index(op.f('ix_tasks_org_id'), 'tasks', ['org_id'], unique=False)
    op.create_index(op.f('ix_tasks_meeting_id'), 'tasks', ['meeting_id'], unique=False)
    op.create_index(op.f('ix_tasks_status'), 'tasks', ['status'], unique=False)
    op.create_index(op.f('ix_tasks_owner_user_id'), 'tasks', ['owner_user_id'], unique=False)

    # Usage Meters
    op.create_table(
        'usage_meters',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.Integer(), nullable=False),
        sa.Column('period_month', sa.String(), nullable=False),
        sa.Column('audio_minutes', sa.Float(), nullable=False),
        sa.Column('tokens_in', sa.Integer(), nullable=False),
        sa.Column('tokens_out', sa.Integer(), nullable=False),
        sa.Column('storage_mb', sa.Float(), nullable=False),
        sa.Column('cost_estimate', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usage_meters_id'), 'usage_meters', ['id'], unique=False)
    op.create_index(op.f('ix_usage_meters_org_id'), 'usage_meters', ['org_id'], unique=False)
    op.create_index(op.f('ix_usage_meters_period_month'), 'usage_meters', ['period_month'], unique=False)

    # Provider Events
    op.create_table(
        'provider_events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.Integer(), nullable=False),
        sa.Column('provider', sa.String(), nullable=False),
        sa.Column('model', sa.String(), nullable=False),
        sa.Column('latency_ms', sa.Float(), nullable=False),
        sa.Column('tokens_in', sa.Integer(), nullable=False),
        sa.Column('tokens_out', sa.Integer(), nullable=False),
        sa.Column('cost_usd', sa.Float(), nullable=False),
        sa.Column('success', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_events_id'), 'provider_events', ['id'], unique=False)
    op.create_index(op.f('ix_provider_events_org_id'), 'provider_events', ['org_id'], unique=False)
    op.create_index(op.f('ix_provider_events_provider'), 'provider_events', ['provider'], unique=False)
    op.create_index(op.f('ix_provider_events_created_at'), 'provider_events', ['created_at'], unique=False)

    # Redaction Vaults
    op.create_table(
        'redaction_vaults',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('org_id', sa.Integer(), nullable=False),
        sa.Column('token', sa.String(), nullable=False),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('value_ciphertext', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['org_id'], ['organizations.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_redaction_vaults_id'), 'redaction_vaults', ['id'], unique=False)
    op.create_index(op.f('ix_redaction_vaults_org_id'), 'redaction_vaults', ['org_id'], unique=False)
    op.create_index(op.f('ix_redaction_vaults_token'), 'redaction_vaults', ['token'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_redaction_vaults_token'), table_name='redaction_vaults')
    op.drop_index(op.f('ix_redaction_vaults_org_id'), table_name='redaction_vaults')
    op.drop_index(op.f('ix_redaction_vaults_id'), table_name='redaction_vaults')
    op.drop_table('redaction_vaults')
    op.drop_index(op.f('ix_provider_events_created_at'), table_name='provider_events')
    op.drop_index(op.f('ix_provider_events_provider'), table_name='provider_events')
    op.drop_index(op.f('ix_provider_events_org_id'), table_name='provider_events')
    op.drop_index(op.f('ix_provider_events_id'), table_name='provider_events')
    op.drop_table('provider_events')
    op.drop_index(op.f('ix_usage_meters_period_month'), table_name='usage_meters')
    op.drop_index(op.f('ix_usage_meters_org_id'), table_name='usage_meters')
    op.drop_index(op.f('ix_usage_meters_id'), table_name='usage_meters')
    op.drop_table('usage_meters')
    op.drop_index(op.f('ix_tasks_owner_user_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_status'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_meeting_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_org_id'), table_name='tasks')
    op.drop_index(op.f('ix_tasks_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_insights_owner_user_id'), table_name='insights')
    op.drop_index(op.f('ix_insights_type'), table_name='insights')
    op.drop_index(op.f('ix_insights_meeting_id'), table_name='insights')
    op.drop_index(op.f('ix_insights_id'), table_name='insights')
    op.drop_table('insights')
    op.drop_index(op.f('ix_utterances_speaker_id'), table_name='utterances')
    op.drop_index(op.f('ix_utterances_meeting_id'), table_name='utterances')
    op.drop_index(op.f('ix_utterances_id'), table_name='utterances')
    op.drop_table('utterances')
    op.drop_index(op.f('ix_speakers_meeting_id'), table_name='speakers')
    op.drop_index(op.f('ix_speakers_id'), table_name='speakers')
    op.drop_table('speakers')
    op.drop_index(op.f('ix_meetings_calendar_event_id'), table_name='meetings')
    op.drop_index(op.f('ix_meetings_status'), table_name='meetings')
    op.drop_index(op.f('ix_meetings_occurred_at'), table_name='meetings')
    op.drop_index(op.f('ix_meetings_org_id'), table_name='meetings')
    op.drop_index(op.f('ix_meetings_id'), table_name='meetings')
    op.drop_table('meetings')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_org_id'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_organizations_domain'), table_name='organizations')
    op.drop_index(op.f('ix_organizations_name'), table_name='organizations')
    op.drop_index(op.f('ix_organizations_id'), table_name='organizations')
    op.drop_table('organizations')

