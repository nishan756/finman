from .views import Home,member_list,member_detail,create_member,edit_member,delete_member,create_payment_context,edit_payment_context,all_payment_context,payment_context_detail,delete_payment_context,create_member_transaction,edit_member_transaction,all_member_transaction,member_transaction_detail,delete_member_transaction,transaction_list,transaction_detail,create_transaction,delete_transaction,edit_transaction,ClubList,ClubProfile
from django.urls import path

urlpatterns = [

    path('home/',Home,name = 'home'),
    # Start member related links
    path('member-list/',member_list,name = 'member-list'),
    path('member-detail/<str:id>/',member_detail,name = 'member-detail'),
    path('create-member/',create_member,name = 'create-member'),
    path('edit-member/<str:id>/',edit_member,name = 'edit-member'),
    path('delete-member/<str:id>/',delete_member,name = 'delete-member'),
    
    #Start payment conetxt related links 
    path('create-payment-context/',create_payment_context,name = 'create-payment-context'),
    path('edit-payment-context/<str:id>/',edit_payment_context,name = 'edit-payment-context'),
    path('payment-context-list/',all_payment_context,name = 'payment-context-list'),
    path('payment-context-detail/<str:id>/',payment_context_detail,name = 'payment-context-detail'),
    path('delete-payment-context/<str:id>/',delete_payment_context,name = 'delete-payment-context'),

    # Start member transaction details related links
    path('create-member-transaction/',create_member_transaction,name = 'create-member-transaction'),
    path('edit-member-transaction/<str:id>/',edit_member_transaction,name = 'edit-member-transaction'),
    path('member-transaction-list/',all_member_transaction,name = 'member-transaction-list'),
    path('member-transaction-detail/<str:id>/',member_transaction_detail,name = 'member-transaction-detail'),
    path('delete-member-transaction/<str:id>/',delete_member_transaction,name = 'delete-transaction'),

    # Start transaction realted links
    path('create-transaction/',create_transaction,name = 'create-transaction'),
    path('edit-transaction/<str:id>/',edit_transaction,name = 'edit-transaction'),
    path('transaction-list/',transaction_list,name = 'transaction-list'),
    path('transaction-detail/<str:id>/',transaction_detail,name = 'transaction-detail'),
    path('delete-transaction/<str:id>/',delete_transaction,name = 'delete-transaction'),

    # Club list
    path('club-list/',ClubList,name='club_list'),
    path('club-profile/<int:id>/',ClubProfile,name='club_profile'),

]