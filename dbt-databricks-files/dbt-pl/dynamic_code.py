folder=[i.name.rstrip('/') for i in dbutils.fs.ls('s3://de-prj/')]
from pyspark import pipelines as dp

def stream_tables(f):
        @dp.table(name=f'dbt_bmodel_project.bronze.br_{f}')
        def tbl():
            return(
            spark.readStream.format('cloudFiles').option('cloudFiles.format','csv') \
            .option('header','true').option('checkpointLocation',f'/Volumes/workspace/default/my_files/{f}_schema/') \
            .option('inferColumnsType','true').option('mergeSchema','true').load(f's3://de-prj/{f}'))

for f in folder:
    stream_tables(f)