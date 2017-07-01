from enum import Enum


class RequestKeys(Enum):
    PRODUCT_ID = 'productId'
    NUMBER_OF_PRODUCTS = 'noOfProducts'


class SuccesMessages(Enum):
    PRODUCT_ASSIGNED = 'Product assigned to the user'
    PRODUCT_REDEEMED = 'Product is dropped at the Recycle location. You\'ve now earned %d points'
    PROMOCODE_ADDED = 'Promo code applied successfully'


class FailureMessages(Enum):
    INVALID_PROMO_CODE = 'Invalid promo code'
    INVALID_INPUT = 'Invalid input'
    USER_ALREADY_LINKED = 'Invalid operation.User has been already linked to the product.'
    INACTIVE_PRODUCT = 'Inactive product'
    CORRUPTED_PRODUCT = ' Corrupted Product or Product hasn\'t been purchased'
    PROMOCODE_ALREADY_USED = 'Promo code already used'
    PROMOCODE_CANNOT_BE_EMPTY = 'Promo code cannot be empty'
    PRODUCT_IN_USE = "Expired Product or Product already in use"
