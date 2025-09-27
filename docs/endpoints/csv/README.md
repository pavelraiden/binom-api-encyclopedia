# Csv API Endpoints

7 endpoints for csv operations.

## Endpoints

### DELETE /public/api/v1/csv/clicklog/clear

**Description**: Delete all clicklog files.

**Documentation**: [delete_public_api_v1_csv_clicklog_clear.md](delete_public_api_v1_csv_clicklog_clear.md)

---

### DELETE /public/api/v1/csv/conversions/clear

**Description**: Delete all conversion files.

**Documentation**: [delete_public_api_v1_csv_conversions_clear.md](delete_public_api_v1_csv_conversions_clear.md)

---

### GET /public/api/v1/csv/file/{filename}

**Description**: Download file by name.

**Documentation**: [get_public_api_v1_csv_file_filename.md](get_public_api_v1_csv_file_filename.md)

---

### DELETE /public/api/v1/csv/file/{filename}

**Description**: Delete file by name.

**Documentation**: [delete_public_api_v1_csv_file_filename.md](delete_public_api_v1_csv_file_filename.md)

---

### POST /public/api/v1/csv/task/dequeue/{id}

**Description**: Remove task from the queue.

**Documentation**: [post_public_api_v1_csv_task_dequeue_id.md](post_public_api_v1_csv_task_dequeue_id.md)

---

### POST /public/api/v1/csv/task/enqueue

**Description**: Add new task to the queue.

**Documentation**: [post_public_api_v1_csv_task_enqueue.md](post_public_api_v1_csv_task_enqueue.md)

---

### GET /public/api/v1/csv/files

**Description**: Get csv files.

**Documentation**: [get_public_api_v1_csv_files.md](get_public_api_v1_csv_files.md)

---

