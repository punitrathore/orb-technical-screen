# Productionizing our credits service

## Summary

Now that we've started to build out our credits service, we'd love to get it into production.
This means that we've got to think about many things including:

1. SQL database schema modeling
2. Scaling our service
3. And more!

You'll work with your interviewer to talk about how we could design a SQL database schema that would allow us to efficiently bring your service to life.
The scaffolding for this schema will be below and you'll collaborate with your interview to amend this document to map to something that we'd feel comfortable shipping in production!

### What we're looking for (copied from `README.md`)

In order of importance, we’re looking for the following in this section of the interview:

- An ability to talk through SQL database schema design
- An ability to talk through scaling a SQL database

## Requirements

### Summary

Our implementation must do the following (details expanded upon below):

1. Track credit blocks and deductions in the database
2. Support multiple users and tenants
3. Ensure efficient access to data at scale for common use cases like balance calculations

You must amend the existing SQL database schema (below) to handle the above requirements.
You are allowed to add / edit / remove any tables, columns, and indexes as needed to satisfy the requirements above.

## Details

### Database Schema

Below, we have provided the beginning scaffolding of a database schema for two database tables.
We made a few simplifying assumptions when debugging our code that we'd now like to address, these include:

- We will need to make sure we scope our credits and deductions to a specific user
- We will need to think about time as timestamps instead of "seconds since the process started"

In addition to the two tables below, we also have a `user` table that tracks each user whose credits we are tracking and a `tenants` table that tracks individual tenants within our system.
These tables are left out and you don't need to worry about their schemas other than to know that they both have an `id` column that foreign keys can map to.
You can think of a tenant as a company that buys Orb's product (e.g. Acme Corporation) and a user as someone who buys the tenant's product (i.e. a customer of Acme Corporation).

### Credits Table

#### Schema

| Column name | Data type | Notes                                       |
| ----------- | --------- | ------------------------------------------- |
| id          | UUID      | UUIDv4 generated from the database directly |
| tenant_id   | UUID      | Foreign key to our `tenants` table          |
| user_id | UUID | Foreign key to our `users` table |
| created_at  | timestamp | Default to `NOW()` if unset                 |
| amount | BIGDECIMAL |
| effective_at | timestamp |
| expires_at | timestamp | 


#### queries

select * from credits where user_id = ? and tenant_id = ? and effective_at <= ?

#### Indexes

| Index field(s) | Index type  |
| -------------- | ----------- |
| id             | Primary Key |
| tenant_id      | Regular     |
| tenant_id, user_id, effective_at  | BTree  |

### Deductions Table

#### Schema

| Column name | Data type | Notes                                       |
| ----------- | --------- | ------------------------------------------- |
| id          | UUID      | UUIDv4 generated from the database directly |
| tenant_id   | UUID      | Foreign key to our `tenants` table          |
| user_id | UUID | foreign key from `users` 
| created_at  | timestamp | Default to `NOW()` if unset                 |
| amount | BIGDECIMAL |
| effective_at | timestamp |

### queries
select * from deductions where user_id = ? and tenant_id = ? and effective_at <= timestamp



#### Indexes

| Index field(s) | Index type  |
| -------------- | ----------- |
| id             | Primary Key |
| tenant_id      | Regular     |
| tenant_id, user_id, effective_at | BTree
