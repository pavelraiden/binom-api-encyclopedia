# Affiliate Network API Guide

## Overview
This guide covers all 10 endpoints in the affiliate_network category.

## Endpoints in this category:

### GET /public/api/v1/affiliate_network/{id}/clone
**Summary**: Clone Affiliate Network
**Description**: Clone Affiliate Network. Retrieves information from the affiliate_network resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving network details for campaign setup or auditing

### POST /public/api/v1/affiliate_network
**Summary**: Create Affiliate Network
**Description**: Creates a new affiliate network with comprehensive configuration including postback URLs, IP whitelist for security, payout relations mapping, and activation settings. This is typically the first step...
**Workflow**: First step: Create affiliate network before adding offers and campaigns

### GET /public/api/v1/affiliate_network/{id}
**Summary**: Get Affiliate Network
**Description**: Retrieves complete information about a specific affiliate network including all configuration parameters, postback settings, payout relations, and current status. Essential for auditing and managing e...
**Workflow**: Used for: Retrieving network details for campaign setup or auditing

### PUT /public/api/v1/affiliate_network/{id}
**Summary**: Edit Affiliate Network
**Description**: Edit Affiliate Network. Updates an existing affiliate_network resource with new configuration data....
**Workflow**: Used for: Updating network configuration or postback settings

### DELETE /public/api/v1/affiliate_network/{id}
**Summary**: Delete Affiliate Network
**Description**: Delete Affiliate Network. Removes a affiliate_network resource (typically soft delete that can be restored)....
**Workflow**: Used for: Removing unused networks (can be restored later)

### PATCH /public/api/v1/affiliate_network/{id}
**Summary**: Restore Affiliate Network
**Description**: Restore Affiliate Network. Partially updates or restores a affiliate_network resource....
**Workflow**: Part of affiliate_network management workflow

### GET /public/api/v1/affiliate_network/list/filtered
**Summary**: Get Affiliate Network list filtered
**Description**: Get Affiliate Network list filtered. Retrieves information from the affiliate_network resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving network details for campaign setup or auditing

### GET /public/api/v1/affiliate_network/list/all
**Summary**: Get Affiliate Network list
**Description**: Get Affiliate Network list. Retrieves information from the affiliate_network resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving network details for campaign setup or auditing

### GET /public/api/v1/affiliate_network/preset/catalog
**Summary**: Get Affiliate Network presets
**Description**: Get Affiliate Network presets. Retrieves information from the affiliate_network resource with optional filtering and pagination....
**Workflow**: Used for: Retrieving network details for campaign setup or auditing

### PUT /public/api/v1/affiliate_network/{id}/rename
**Summary**: Rename Affiliate Network
**Description**: Rename Affiliate Network. Updates an existing affiliate_network resource with new configuration data....
**Workflow**: Used for: Updating network configuration or postback settings

