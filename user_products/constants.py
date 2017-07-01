from enum import Enum


class RequestKeys(Enum):
    PRODUCT_ID = 'productId'
    NUMBER_OF_PRODUCTS = 'noOfProducts'


class SuccesMessages(Enum):
    PRODUCT_ASSIGNED = 'Product assigned to the user'
    PROMOCODE_ADDED = 'Promo code applied successfully'


class FailureMessages(Enum):
    INVALID_PROMO_CODE = 'Invalid promo code'
    INVALID_INPUT = 'Promo type id or number of promo codes to generate cannot be empty'
    PROMOCODE_ALREADY_USED = 'Promo code already used'
    PROMOCODE_CANNOT_BE_EMPTY = 'Promo code cannot be empty'
    PRODUCT_IN_USE = "Invalid Product or Product already in use"
