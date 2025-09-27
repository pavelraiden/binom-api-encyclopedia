# Campaign API Guide

## Overview
This guide covers all 27 endpoints in the campaign category.

## Endpoints in this category:

### POST /public/api/v1/campaign
**Summary**: Create Campaign
**Description**: Creates a new tracking campaign with specified traffic source, cost model, landing pages, and offers. This is the core operation for setting up traffic tracking and requires careful configuration of a...
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### GET /public/api/v1/campaign/{id}
**Summary**: Get Campaign
**Description**: Fetches complete campaign configuration including traffic source settings, landing page rotations, offer assignments, cost models, and current status. Critical for campaign management and troubleshoot...
**Workflow**: Used for: Retrieving campaign details for optimization or troubleshooting

### PUT /public/api/v1/campaign/{id}
**Summary**: Edit Campaign
**Description**: Edit Campaign. Updates an existing campaign resource with new configuration data....
**Workflow**: Used for: Updating campaign settings, costs, or routing rules

### DELETE /public/api/v1/campaign/{id}
**Summary**: Delete Campaign
**Description**: Delete Campaign. Removes a campaign resource (typically soft delete that can be restored)....
**Workflow**: Used for: Pausing or removing campaigns (can be restored)

### PATCH /public/api/v1/campaign/{id}
**Summary**: Restore Campaign
**Description**: Restore Campaign. Partially updates or restores a campaign resource....
**Workflow**: Part of campaign management workflow

### GET /public/api/v1/campaign/{id}/clone
**Summary**: Clone Campaign
**Description**: Clone Campaign. Retrieves information from the campaign resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving campaign details for optimization or troubleshooting

### PUT /public/api/v1/campaign/{id}/rename
**Summary**: Rename Campaign
**Description**: Rename Campaign. Updates an existing campaign resource with new configuration data....
**Workflow**: Used for: Updating campaign settings, costs, or routing rules

### PATCH /public/api/v1/campaign/modify/{id}
**Summary**: Modify Campaign
**Description**: Modify Campaign. Partially updates or restores a campaign resource....
**Workflow**: Part of campaign management workflow

### GET /public/api/v1/campaign/{id}/link
**Summary**: Get Campaign Link
**Description**: Get Campaign Link. Retrieves information from the campaign resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving campaign details for optimization or troubleshooting

### GET /public/api/v1/campaign/list/filtered
**Summary**: Get Campaign list filtered
**Description**: Get Campaign list filtered. Retrieves information from the campaign resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving campaign details for optimization or troubleshooting

### GET /public/api/v1/campaign/short/info
**Summary**: Get Campaign short info
**Description**: Get Campaign short info. Retrieves information from the campaign resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving campaign details for optimization or troubleshooting

### GET /public/api/v1/campaign/by_rotation/{rotationId}/list
**Summary**: Get Campaign list by rotation
**Description**: Get Campaign list by rotation. Retrieves information from the campaign resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving campaign details for optimization or troubleshooting

### GET /public/api/v1/campaign/traffic_source/list
**Summary**: Get Campaign traffic source list
**Description**: Get Campaign traffic source list. Retrieves information from the campaign resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving campaign details for optimization or troubleshooting

### POST /public/api/v1/campaign/change_setting
**Summary**: Change Campaign Setting
**Description**: Change Campaign Setting. Creates a new campaign resource with specified configuration parameters....
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### POST /public/api/v1/campaign/change_cost
**Summary**: Change Campaign Cost
**Description**: Change Campaign Cost. Creates a new campaign resource with specified configuration parameters....
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### POST /public/api/v1/campaign/change_domain
**Summary**: Change Campaign Domain
**Description**: Change Campaign Domain. Creates a new campaign resource with specified configuration parameters....
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### POST /public/api/v1/campaign/change_group
**Summary**: Change Campaign Group
**Description**: Change Campaign Group. Creates a new campaign resource with specified configuration parameters....
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### POST /public/api/v1/campaign/switch_domain
**Summary**: Switch Campaign Domain
**Description**: Switch Campaign Domain. Creates a new campaign resource with specified configuration parameters....
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### POST /public/api/v1/campaign/change_traffic_distribution_info
**Summary**: Change Campaign Traffic Distribution Info
**Description**: Change Campaign Traffic Distribution Info. Creates a new campaign resource with specified configuration parameters....
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### PUT /public/api/v1/campaign/landing/pause
**Summary**: Pause Campaign Landing
**Description**: Pause Campaign Landing. Updates an existing campaign resource with new configuration data....
**Workflow**: Used for: Updating campaign settings, costs, or routing rules

### PUT /public/api/v1/campaign/offer/pause
**Summary**: Pause Campaign Offer
**Description**: Pause Campaign Offer. Updates an existing campaign resource with new configuration data....
**Workflow**: Used for: Updating campaign settings, costs, or routing rules

### PUT /public/api/v1/campaign/path/pause
**Summary**: Pause Campaign Path
**Description**: Pause Campaign Path. Updates an existing campaign resource with new configuration data....
**Workflow**: Used for: Updating campaign settings, costs, or routing rules

### GET /public/api/v1/campaign/{id}/permissions
**Summary**: Get Campaign Permissions
**Description**: Get Campaign Permissions. Retrieves information from the campaign resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving campaign details for optimization or troubleshooting

### POST /public/api/v1/campaign/{id}/permissions
**Summary**: Grant Campaign Permissions
**Description**: Grant Campaign Permissions. Creates a new campaign resource with specified configuration parameters....
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### DELETE /public/api/v1/campaign/{id}/permissions
**Summary**: Revoke Campaign Permissions
**Description**: Revoke Campaign Permissions. Removes a campaign resource (typically soft delete that can be restored)....
**Workflow**: Used for: Pausing or removing campaigns (can be restored)

### POST /public/api/v1/campaign/{campaignId}/owner
**Summary**: Change Campaign Owner
**Description**: Change Campaign Owner. Creates a new campaign resource with specified configuration parameters....
**Workflow**: Core step: Create campaign after setting up traffic sources and networks

### DELETE /public/api/v1/campaign/{campaignId}/owner
**Summary**: Delete Campaign Owner
**Description**: Delete Campaign Owner. Removes a campaign resource (typically soft delete that can be restored)....
**Workflow**: Used for: Pausing or removing campaigns (can be restored)

