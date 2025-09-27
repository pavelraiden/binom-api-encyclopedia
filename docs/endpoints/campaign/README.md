# Campaign API Endpoints

24 endpoints for campaign operations.

## Endpoints

### POST /public/api/v1/campaign/change_setting

**Description**: Edit Settings for multiple Campaigns

**Documentation**: [post_public_api_v1_campaign_change_setting.md](post_public_api_v1_campaign_change_setting.md)

---

### POST /public/api/v1/campaign/change_cost

**Description**: Change cost for multiple Campaigns

**Documentation**: [post_public_api_v1_campaign_change_cost.md](post_public_api_v1_campaign_change_cost.md)

---

### POST /public/api/v1/campaign/change_domain

**Description**: Change Domain for multiple Campaigns

**Documentation**: [post_public_api_v1_campaign_change_domain.md](post_public_api_v1_campaign_change_domain.md)

---

### POST /public/api/v1/campaign/change_group

**Description**: Change Group for multiple Campaigns

**Documentation**: [post_public_api_v1_campaign_change_group.md](post_public_api_v1_campaign_change_group.md)

---

### POST /public/api/v1/campaign/{campaignId}/owner

**Description**: Change Campaign Owner

**Documentation**: [post_public_api_v1_campaign_campaignId_owner.md](post_public_api_v1_campaign_campaignId_owner.md)

---

### DELETE /public/api/v1/campaign/{campaignId}/owner

**Description**: Delete Campaign Owner

**Documentation**: [delete_public_api_v1_campaign_campaignId_owner.md](delete_public_api_v1_campaign_campaignId_owner.md)

---

### POST /public/api/v1/campaign/change_traffic_distribution_info

**Description**: Change TrafficDistributionInfo for multiple Campaigns

**Documentation**: [post_public_api_v1_campaign_change_traffic_distribution_info.md](post_public_api_v1_campaign_change_traffic_distribution_info.md)

---

### GET /public/api/v1/campaign/{id}/clone

**Description**: Clone Campaign.

**Documentation**: [get_public_api_v1_campaign_id_clone.md](get_public_api_v1_campaign_id_clone.md)

---

### POST /public/api/v1/campaign

**Description**: Create Campaign.

**Documentation**: [post_public_api_v1_campaign.md](post_public_api_v1_campaign.md)

---

### GET /public/api/v1/campaign/{id}

**Description**: Get Campaign.

**Documentation**: [get_public_api_v1_campaign_id.md](get_public_api_v1_campaign_id.md)

---

### PUT /public/api/v1/campaign/{id}

**Description**: Edit Campaign.

**Documentation**: [put_public_api_v1_campaign_id.md](put_public_api_v1_campaign_id.md)

---

### DELETE /public/api/v1/campaign/{id}

**Description**: Delete Campaign.

**Documentation**: [delete_public_api_v1_campaign_id.md](delete_public_api_v1_campaign_id.md)

---

### PATCH /public/api/v1/campaign/{id}

**Description**: Restore Campaign.

**Documentation**: [patch_public_api_v1_campaign_id.md](patch_public_api_v1_campaign_id.md)

---

### GET /public/api/v1/campaign/{id}/link

**Description**: Get Campaign link.

**Documentation**: [get_public_api_v1_campaign_id_link.md](get_public_api_v1_campaign_id_link.md)

---

### GET /public/api/v1/campaign/list/filtered

**Description**: Get Campaign list filtered.

**Documentation**: [get_public_api_v1_campaign_list_filtered.md](get_public_api_v1_campaign_list_filtered.md)

---

### GET /public/api/v1/campaign/short/info

**Description**: Get Campaign short info with links.

**Documentation**: [get_public_api_v1_campaign_short_info.md](get_public_api_v1_campaign_short_info.md)

---

### GET /public/api/v1/campaign/by_rotation/{rotationId}/list

**Description**: Get Campaigns list by Rotation ID.

**Documentation**: [get_public_api_v1_campaign_by_rotation_rotationId_list.md](get_public_api_v1_campaign_by_rotation_rotationId_list.md)

---

### GET /public/api/v1/campaign/traffic_source/list

**Description**: Get TrafficSource with Campaign list.

**Documentation**: [get_public_api_v1_campaign_traffic_source_list.md](get_public_api_v1_campaign_traffic_source_list.md)

---

### GET /public/api/v1/campaign/{id}/permissions

**Description**: Get users with Permission access to the passed Campaign

**Documentation**: [get_public_api_v1_campaign_id_permissions.md](get_public_api_v1_campaign_id_permissions.md)

---

### POST /public/api/v1/campaign/{id}/permissions

**Description**: Grant user access to the specified campaign

**Documentation**: [post_public_api_v1_campaign_id_permissions.md](post_public_api_v1_campaign_id_permissions.md)

---

### DELETE /public/api/v1/campaign/{id}/permissions

**Description**: Revoke users access to the specified campaign

**Documentation**: [delete_public_api_v1_campaign_id_permissions.md](delete_public_api_v1_campaign_id_permissions.md)

---

### PATCH /public/api/v1/campaign/modify/{id}

**Description**: Partially update Campaign.

**Documentation**: [patch_public_api_v1_campaign_modify_id.md](patch_public_api_v1_campaign_modify_id.md)

---

### PUT /public/api/v1/campaign/{id}/rename

**Description**: Rename Campaign.

**Documentation**: [put_public_api_v1_campaign_id_rename.md](put_public_api_v1_campaign_id_rename.md)

---

### POST /public/api/v1/campaign/switch_domain

**Description**: Change Domain for multiple Campaigns

**Documentation**: [post_public_api_v1_campaign_switch_domain.md](post_public_api_v1_campaign_switch_domain.md)

---

