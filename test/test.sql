create schema kudu.test;

use kudu.test;


create table t1
(
    id   int with(primary_key= true),
    name varchar
)
with (
    partition_by_hash_columns = ARRAY['id'],
    partition_by_hash_buckets = 2
);

insert into t1
values (1, 'a');
insert into t1
values (1, 'b');

select *
from t1;
