Copy_options = {
  "kafka": {
    "source_options": {
        "topic_name": {"type": "text", "editable": False, "optional": False},
        "topic": {"type": "text", "editable": False, "optional": False}},
    "job_options": {
        "consumer_properties": {"type": "text", "editable": True, "optional": True},
        "reader_shards": {"type": "integer", "editable": True, "optional": True},
        "store_raw_data": {"type": "value", "editable": False, "optional": True},
        "start_from": {"type": "value", "editable": False, "optional": True},
        "end_at": {"type": "value", "editable": True, "optional": True},
        "compute_cluster": {"type": "identifier", "editable": True, "optional": True},
        "run_parallelism": {"type": "integer", "editable": True, "optional": True},
        "content_type": {"type": "value", "editable": True, "optional": True},
        "compression": {"type": "value", "editable": False, "optional": True},
        "comment": {"type": "text", "editable": True, "optional": True}
    }
  },
  "my_sql": {
    "source_options": {
        "table_include_list": {"type": "text", "editable": True, "optional": True},
        "column_exclude_list": {"type": "text", "editable": True, "optional": True}
    },
    "job_options": {
        "skip_snapshots": {"value": "text", "editable": True, "optional": True},
        "end_at": {"type": "value", "editable": True, "optional": True},
        "compute_cluster": {"type": "identifier", "editable": True, "optional": True},
        "comment": {"type": "text", "editable": True, "optional": True}
    }
  },
  "postgre_sql": {
    "source_options": {
        "bucket": {"type": "text", "editable": False, "optional": False},
        "prefix": {"type": "text", "editable": False, "optional": True}
    },
    "job_options": {
        "table_include_list": {"type": "text", "editable": False, "optional": True},
        "skip_snapshots": {"type": "boolean", "editable": False, "optional": True},
        "column_exclude_list": {"type": "text", "editable": False, "optional": True},
        "publication_name": {"type": "text", "editable": False, "optional": False},
        "file_pattern": {"type": "text", "editable": False, "optional": True},
        "delete_files_after_load": {"type": "boolean", "editable": False, "optional": True},
        "end_at": {"type": "value", "editable": True, "optional": True},
        "compute_cluster": {"type": "identifier", "editable": True, "optional": True},
        "run_parallelism": {"type": "integer", "editable": True, "optional": True},
        "comment": {"type": "text", "editable": True, "optional": True}
    }
  },
  "s3": {
    "source_options": {
        "location": {"type": "text", "editable": False, "optional": False}
    },
    "job_options": {
        "file_pattern": {"type": "text", "editable": False, "optional": True},
        "delete_files_after_load": {"type": "boolean", "editable": False, "optional": True},
        "end_at": {"type": "value", "editable": True, "optional": True},
        "compute_cluster": {"type": "identifier", "editable": True, "optional": True},
        "run_parallelism": {"type": "integer", "editable": True, "optional": True},
        "content_type": {"type": "value", "editable": True, "optional": True},
        "compression": {"type": "value", "editable": False, "optional": True},
        "comment": {"type": "text", "editable": True, "optional": True}
    }
  }
}
