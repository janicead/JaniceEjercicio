import json

from app import app, shipping_merchants
import pytest
import unittest

def test_same_shipping_cost_and_estimated_delivery_dates(mocker):
    mocker.patch("app._get_shipping_options", return_value={
      "shipping_options": [
        {
          "name": "Option 1",
          "type": "Delivery",
          "cost": 10,
          "estimated_days": 3
        },
        {
          "name": "Option 2",
          "type": "Custom",
          "cost": 10,
          "estimated_days": 3
        },
        {
          "name": "Option 3",
          "type": "Pickup",
          "cost": 10,
          "estimated_days": 3
        }
      ]
    })

    assert shipping_merchants().status_code == 200
    assert shipping_merchants().json == [
        {"name": "Option 1", "type": "Delivery", "cost": 10, "estimated_days": 3},
        {"name": "Option 2", "type": "Custom", "cost": 10, "estimated_days": 3},
        {"name": "Option 3", "type": "Pickup", "cost": 10, "estimated_days": 3}
    ]

def test_same_shipping_cost_and_different_estimated_delivery_dates(mocker):
    mocker.patch("app._get_shipping_options", return_value={
      "shipping_options": [
          {"name":"Option 1","type":"Delivery","cost":10,"estimated_days":5},
          {"name":"Option 2","type":"Custom","cost":10,"estimated_days":2},
          {"name":"Option 3","type":"Pickup","cost":10,"estimated_days":3}]
    })

    assert shipping_merchants().status_code == 200
    assert shipping_merchants().json == [
        {"name":"Option 2","type":"Custom","cost":10,"estimated_days":2},
        {"name":"Option 3","type":"Pickup","cost":10,"estimated_days":3},
        {"name":"Option 1","type":"Delivery","cost":10,"estimated_days":5}]

def test_different_shipping_cost_and_same_estimated_delivery_dates(mocker):
    mocker.patch("app._get_shipping_options", return_value={
      "shipping_options": [
          {"name":"Option 1","type":"Delivery","cost":6,"estimated_days":3},
          {"name":"Option 2","type":"Custom","cost":5,"estimated_days":3},
          {"name":"Option 3","type":"Pickup","cost":10,"estimated_days":3}]
    })

    assert shipping_merchants().status_code == 200
    assert shipping_merchants().json == [
        {"name":"Option 2","type":"Custom","cost":5,"estimated_days":3},
        {"name":"Option 1","type":"Delivery","cost":6,"estimated_days":3},
        {"name":"Option 3","type":"Pickup","cost":10,"estimated_days":3}]

def test_different_shipping_cost_and_different_estimated_delivery_dates(mocker):
    mocker.patch("app._get_shipping_options", return_value={
      "shipping_options": [
          {"name":"Option 1","type":"Delivery","cost":10,"estimated_days":5},
          {"name":"Option 2","type":"Custom","cost":5,"estimated_days":3},
          {"name":"Option 3","type":"Pickup","cost":7,"estimated_days":2}]
    })

    assert shipping_merchants().status_code == 200
    assert shipping_merchants().json == [
        {"name":"Option 2","type":"Custom","cost":5,"estimated_days":3},
        {"name":"Option 3","type":"Pickup","cost":7,"estimated_days":2},
        {"name":"Option 1","type":"Delivery","cost":10,"estimated_days":5}]

def test_no_shipping_options(mocker):
    mocker.patch("app._get_shipping_options", return_value={
      "shipping_options": []
    })

    assert shipping_merchants().status_code == 200
    assert shipping_merchants().json == []