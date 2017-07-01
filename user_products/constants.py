from enum import Enum


class RequestKeys(Enum):
    PRODUCT_ID = 'productId'
    NUMBER_OF_PRODUCTS = 'noOfProducts'


class ResponseKeys(Enum):
    CATEGORIES = 'categories'
    USER_POINTS = 'userPoints'
    ID = 'id'
    COMPLETED_COUNT = 'completedCount'
    ACTIVE_COUNT = 'activeCount'
    TOTAL_COMPLETED_COUNT = 'totalCompletedCount'
    TOTAL_ACTIVE_COUNT = 'totalActiveCount'


class SuccesMessages(Enum):
    PRODUCT_ASSIGNED = 'Product assigned to the user'
    PRODUCT_REDEEMED = 'Thank you for joining the movement. You now have %d points'
    PROMOCODE_ADDED = 'Promo code applied successfully'
    REDEEM_MESSAGE = '%s , you\'ve made it.Hope to see you soon'


class FailureMessages(Enum):
    INVALID_PROMO_CODE = 'Invalid promo code'
    INVALID_INPUT = 'Invalid input'
    USER_ALREADY_LINKED = 'Invalid operation. A user has been already linked to the product.'
    INACTIVE_PRODUCT = 'Inactive product'
    CORRUPTED_PRODUCT = ' Corrupted Product or Product hasn\'t been purchased'
    PROMOCODE_ALREADY_USED = 'Promo code already used'
    PROMOCODE_CANNOT_BE_EMPTY = 'Promo code cannot be empty'
    PRODUCT_IN_USE = "Expired Product or Product already in use"
