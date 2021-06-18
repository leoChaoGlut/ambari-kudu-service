./kudu-cli master run -master_addresses=dmp-kudu001:7051,dmp-kudu002:7051,dmp-kudu003:7051 -fs_wal_dir=/tmp/kudu/master/wal -fs_data_dirs=/tmp/kudu/master/data -fs_metadata_dir=/tmp/kudu/master/metadata

./kudu-cli tserver run -tserver_master_addrs=dmp-kudu001:7051,dmp-kudu002:7051,dmp-kudu003:7051 -fs_wal_dir=/tmp/kudu/tserver/wal -fs_data_dirs=/tmp/kudu/tserver/data -fs_metadata_dir=/tmp/kudu/tserver/metadata

yum install cyrus-sasl-plain -y
yum install cyrus-sasl-plain cyrus-sasl-devel cyrus-sasl-gssapi -y
yum remove cyrus-sasl-plain cyrus-sasl-devel cyrus-sasl-gssapi -y
gcc python-devel cyrus-sasl-devel cyrus-sasl-gssapi


rm -rf /tmp/kudu/master/*
rm -rf /tmp/kudu/tserver/*

mkdir -p /tmp/kudu/tserver/wal



