from django.http import HttpResponseForbidden
from django.shortcuts import render,get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Max,Q
from django.db.models.functions import Coalesce
from django.utils import timezone
from .models import Claim
# Create your views here.
@login_required
def claims_list(request):
    claims=Claim.objects.all().order_by('id')
    status_filter=request.GET.get('status','')
    insurer_filter=request.GET.get('insurer','')
    if status_filter:
        claims = claims.filter(status=status_filter)
    if insurer_filter:
        # Use 'icontains' for a case-insensitive partial match
        claims = claims.filter(insurer_name__icontains=insurer_filter)
    context = {
        'claims': claims,
        'current_status': status_filter,
        'current_insurer': insurer_filter,
        # This line must be present and correct
        'statuses': Claim.Status.choices,
    }
    if claims.exists():
        context['first_claim']=claims.first()

    if request.headers.get('HX-Request'):
        return render(request,'claims/partials/claim_table_rows.html',context)
    return render(request,'claims/claims_list.html',context)
@login_required
def claim_detail(request,claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    context = {
        'claim': claim
    }
    return render(request,'claims/partials/claim_detail.html',context)

@login_required 
@require_POST
def flag_claim(request,claim_id):
    claim = get_object_or_404(Claim, id=claim_id)
    claim.is_flagged = True
    claim.save()
    context = {
        'claim': claim,
    }
    return render(request,'claims/partials/claim_flag_button.html',context)

@login_required
@require_POST
def add_note(request,claim_id):
    claim=get_object_or_404(Claim, id=claim_id)
    note_text=request.POST.get('note_text','').strip()
    if note_text:
        from .models import Note
        Note.objects.create(claim=claim,author=request.user,text=note_text)
    context = {
        'claim': claim,
    }
    return render(request,'claims/partials/claim_note.html',context)

@login_required
def admin_dashboard(request):
    """
    Calculates and displays the 6 key stats for the admin dashboard.
    """
    if not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this page.")

    # Stat 1: Active Backlog
    active_backlog = Claim.objects.filter(status='Under Review').count()

    # Stat 2: Flagged for Review
    flagged_count = Claim.objects.filter(is_flagged=True).count()

    # Stat 3: Potential Recovery
    potential_recovery = Claim.objects.filter(status='Denied').aggregate(
        total=Sum('billed_amount')
    )['total'] or 0

    # Stat 4: Recovered This Month
    now = timezone.now()
    recovered_this_month = Claim.objects.filter(
        status='Paid',
        updated_at__year=now.year,
        updated_at__month=now.month
    ).aggregate(total=(Sum('paid_amount')))['total'] or 0

    # Stat 5: Highest Value Flagged Claim
    highest_flagged = Claim.objects.filter(is_flagged=True).aggregate(
        max_billed=Max('billed_amount')
    )['max_billed'] or 0

    # Stat 6: Overall Denial Rate
    finalized_claims = Claim.objects.filter(Q(status='Paid') | Q(status='Denied'))
    denied_count = finalized_claims.filter(status='Denied').count()
    total_finalized = finalized_claims.count()
    denial_rate = (denied_count / total_finalized * 100) if total_finalized > 0 else 0

    context = {
        'active_backlog': active_backlog,
        'flagged_count': flagged_count,
        'potential_recovery': potential_recovery,
        'recovered_this_month': recovered_this_month,
        'highest_flagged': highest_flagged,
        'denial_rate': denial_rate,
    }
    
    return render(request, 'claims/admin_dashboard.html', context)