from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as sa_pg

__all__ = [
    'sessions_table',
    'permissions_table',
    'groups_table',
    'group_permissions_table',
    'users_table',
    'user_groups_table',
]

permissions_table = sa.Table(
    'permissions',
    sa.MetaData(),
    sa.Column('id', sa.TEXT, primary_key=True, nullable=False),
    sa.Column('enabled', sa.Boolean, nullable=False, default=True),
    sa.Column('tag', sa.TEXT, nullable=True),
    sa.Column('description', sa.TEXT, nullable=True),
)

groups_table = sa.Table(
    'groups',
    sa.MetaData(),
    sa.Column('id', sa.TEXT, primary_key=True, nullable=False),
    sa.Column('tag', sa.TEXT, nullable=True),
    sa.Column('description', sa.TEXT, nullable=True),
)

group_permissions_table = sa.Table(
    'group_permissions',
    sa.MetaData(),
    sa.Column('group_id', sa.TEXT, sa.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    sa.Column(
        'permission_id', sa.TEXT, sa.ForeignKey('permissions.id', ondelete='CASCADE'), nullable=False, primary_key=True
    ),
)

users_table = sa.Table(
    'users',
    sa.MetaData(),
    sa.Column('id', sa_pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')),
    sa.Column('username', sa.TEXT, unique=True, nullable=False),
    sa.Column('email', sa.TEXT, unique=True, nullable=False),
    sa.Column('full_name', sa.TEXT, nullable=True),
    sa.Column('password', sa_pg.BYTEA, nullable=False),
    sa.Column('salt', sa_pg.BYTEA, nullable=False),
    sa.Column('is_active', sa.Boolean, nullable=False, default=True),
    sa.Column('is_blocked', sa.Boolean, nullable=False, default=False),
    sa.Column('settings', sa_pg.JSONB, nullable=False, server_default=sa.text("'{}'::jsonb")),
    sa.Column(
        'created',
        sa.DateTime,
        nullable=False,
        default=datetime.utcnow,
        server_default=sa.func.timezone('UTC', sa.func.current_timestamp()),
    ),
)

user_groups_table = sa.Table(
    'user_groups',
    sa.MetaData(),
    sa.Column('group_id', sa.TEXT, sa.ForeignKey('groups.id', ondelete='CASCADE'), nullable=False, primary_key=True),
    sa.Column(
        'user_id',
        sa_pg.UUID(as_uuid=True),
        sa.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
        primary_key=True,
    ),
)

sessions_table = sa.Table(
    'sessions',
    sa.MetaData(),
    sa.Column('id', sa.TEXT, primary_key=True),
    sa.Column('h_agent', sa_pg.BYTEA, nullable=False),
    sa.Column('user_id', sa_pg.UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
    sa.Column('expires', sa.INTEGER, nullable=False),
    sa.Column('permissions', sa_pg.JSONB, nullable=False),
    sa.Column('data', sa_pg.JSONB, nullable=False),
    sa.Column('created', sa.TIMESTAMP, nullable=False),
)
