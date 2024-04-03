terraform {
  required_version = ">= 1.5.7"
  backend "azurerm" {
    resource_group_name  = "sy4cloud"
    storage_account_name = "sy4tfstate"
    container_name       = "sy4resume-tfstate"
    key                  = "sy4resume-frontend.tfstate"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "sy4rg" {
  name     = "sy4rgresume"
  location = "North Central US"
}

resource "azurerm_storage_account" "sy4sa" {
  name                     = "sy4saresume"
  resource_group_name      = azurerm_resource_group.sy4rg.name
  location                 = azurerm_resource_group.sy4rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"

  static_website {
    index_document     = "index.html"
    error_404_document = "404.html"
  }
}

resource "azurerm_cdn_profile" "sy4cdn-profile" {
  name                = "sy4cdnresume"
  location            = azurerm_resource_group.sy4rg.location
  resource_group_name = azurerm_resource_group.sy4rg.name
  sku                 = "Standard_Microsoft"
}

resource "azurerm_cdn_endpoint" "sy4cdn-endpoint" {
  name                = "sy4endresume"
  profile_name        = azurerm_cdn_profile.sy4cdn-profile.name
  location            = azurerm_resource_group.sy4rg.location
  resource_group_name = azurerm_resource_group.sy4rg.name
  is_http_allowed     = true
  is_https_allowed    = true
  origin_host_header  = azurerm_storage_account.sy4sa.primary_web_host
  content_types_to_compress = [
    "text/html",
    "text/css",
    "application/javascript",
  ]
  querystring_caching_behaviour = "IgnoreQueryString"

  origin {
    name      = "sy4resume"
    host_name = azurerm_storage_account.sy4sa.primary_web_host
  }
}

resource "azurerm_cdn_endpoint_custom_domain" "sy4cdn-custom-domain" {
  name            = "sy4resume"
  cdn_endpoint_id = azurerm_cdn_endpoint.sy4cdn-endpoint.id
  host_name       = "resume.seanyoung.me"

  cdn_managed_https {
    certificate_type = "Dedicated"
    protocol_type    = "ServerNameIndication"
    tls_version      = "TLS12"
  }
}