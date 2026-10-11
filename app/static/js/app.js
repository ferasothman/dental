window.dentalApp = function() {
    return {
        systemInitialized: true,
        isLoggedIn: false,
        currentUser: null,
        currentTab: 'chart',
        financeSubTab: 'patient',

        doctorSetupForm: { full_name: '', username: '', password: '' },
        loginForm: { username: '', password: '' },

        usersList: [],
        showAddUserModal: false,
        showEditUserModal: false,
        newUserForm: { full_name: '', username: '', password: '', role: 'secretary' },
        editUserForm: { id: '', full_name: '', username: '', password: '' },

        conditionsList: [],
        showAddConditionModal: false,
        showEditConditionModal: false,
        newConditionForm: { name: '', color: '#3B82F6', requires_lab: false, default_cost: 0 },
        editConditionForm: { id: '', name: '', color: '#3B82F6', requires_lab: false, default_cost: 0 },

        approvedLabs: [],
        newApprovedLab: { name: '', phone: '', specialty: '' },
        labOrders: [],
        showAddLabModal: false,
        newLabOrder: {
            patient_id: '',
            lab_name: '',
            tooth_number: '',
            work_type: '',
            shade: '',
            sent_date: new Date().toISOString().split('T')[0],
            expected_date: '',
            lab_cost: '',
            patient_price: '',
            notes: ''
        },

        currentPatientXRays: [],
        showAddXRayModal: false,
        viewingXRayImg: null,
        newXRay: { title: '', image_data: '', notes: '' },

        clinicExpenses: [],
        showAddExpenseModal: false,
        newExpense: { title: '', category: 'رواتب وأجور', amount: '', expense_date: new Date().toISOString().split('T')[0], notes: '' },

        reportFilter: {
            start_date: new Date(new Date().getFullYear(), new Date().getMonth(), 1).toISOString().split('T')[0],
            end_date: new Date().toISOString().split('T')[0]
        },
        clinicReport: { total_revenue: 0, total_lab_expenses: 0, total_clinic_expenses: 0, net_profit: 0 },

        patients: [],
        patientSearchTable: '',
        showEditPatientModal: false,
        editPatientForm: { id: '', full_name: '', phone: '', gender: '', age: '', allergies: '', medical_notes: '' },
        duplicateDialog: { show: false, matches: [], name: '', mode: 'create', resolve: null },
        deleteDialog: { show: false, patient: null, impact: null, loading: false, confirmName: '', ack: false, busy: false, error: '' },
        showSessionsHistory: false,
        historyFilter: { q: '', tooth: '' },

        appointments: [],
        appointmentDateFilter: new Date().toISOString().split('T')[0],
        showEditAppointmentModal: false,
        editAppointmentForm: { id: '', appointment_date: '', appointment_time: '', notes: '', status: 'Booked' },

        sessions: [],
        showEditSessionModal: false,
        editSessionForm: { id: '', procedure_name: '', cost: 0, notes: '' },

        showToothSessionsHistoryModal: false,

        financeSummary: { total_cost: 0, total_paid: 0, balance_due: 0, payments: [] },
        currentPatient: null,
        chartData: {},
        focusPart: null,
        selectedTooth: null,
        isSearching: false,
        patientSearchQuery: '',

        showAddAppointmentModal: false,
        showAddPatientModal: false,
        showAddPaymentModal: false,
        appointmentMode: 'existing',
        appointmentPatientSearch: '',
        showAptPatientDropdown: false,

        // تصفير الإجراءات الإضافية بالكامل
        toothForm: { condition: '', crown_condition: 'سليم', root_condition: 'سليم', surfaces: '', cost: 0, notes: '', procedures_summary: '', selectedTags: [] },
        selectedConditionObj: null,
        restoreBackupFile: null,

        newAppointment: { patient_id: '', appointment_date: new Date().toISOString().split('T')[0], appointment_time: '10:00', notes: '' },
        quickPatient: { full_name: '', phone: '', gender: '', age: '' },
        newPatient: { full_name: '', phone: '', gender: '', age: '', allergies: '' },
        newPayment: { amount: '', payment_method: 'Cash', notes: '' },

        upperTeeth: [
            { number: 18 }, { number: 17 }, { number: 16 }, { number: 15 },
            { number: 14 }, { number: 13 }, { number: 12 }, { number: 11 },
            { number: 21 }, { number: 22 }, { number: 23 }, { number: 24 },
            { number: 25 }, { number: 26 }, { number: 27 }, { number: 28 }
        ],
        lowerTeeth: [
            { number: 48 }, { number: 47 }, { number: 46 }, { number: 45 },
            { number: 44 }, { number: 43 }, { number: 42 }, { number: 41 },
            { number: 31 }, { number: 32 }, { number: 33 }, { number: 34 },
            { number: 35 }, { number: 36 }, { number: 37 }, { number: 38 }
        ],

        get filteredPatients() {
            if (!Array.isArray(this.patients)) return [];
            if (!this.patientSearchQuery) return this.patients;
            const q = this.patientSearchQuery.toLowerCase();
            return this.patients.filter(p => (p.full_name || '').toLowerCase().includes(q) || (p.phone || '').includes(q) || this.formatPatientId(p.id).toLowerCase().includes(q));
        },

        get filteredPatientsTable() {
            if (!Array.isArray(this.patients)) return [];
            if (!this.patientSearchTable) return this.patients;
            const q = this.patientSearchTable.toLowerCase();
            return this.patients.filter(p => (p.full_name || '').toLowerCase().includes(q) || (p.phone || '').includes(q) || this.formatPatientId(p.id).toLowerCase().includes(q));
        },

        get searchPatientsForAppointment() {
            if (!Array.isArray(this.patients)) return [];
            if (!this.appointmentPatientSearch) return this.patients;
            const q = this.appointmentPatientSearch.toLowerCase();
            return this.patients.filter(p => (p.full_name || '').toLowerCase().includes(q) || (p.phone || '').includes(q));
        },

        get filteredAppointments() {
            if (!Array.isArray(this.appointments)) return [];
            if (!this.appointmentDateFilter) return this.appointments;
            return this.appointments.filter(a => a.appointment_date === this.appointmentDateFilter);
        },

        get currentPatientLabOrders() {
            if (!this.currentPatient || !Array.isArray(this.labOrders)) return [];
            return this.labOrders.filter(o => o.patient_id === this.currentPatient.id);
        },

        get currentToothSessions() {
            if (!this.selectedTooth || !Array.isArray(this.sessions)) return [];
            return this.sessions.filter(s => String(s.tooth_number) === String(this.selectedTooth.number));
        },

        getToothSessionsCount(num) {
            if (!Array.isArray(this.sessions)) return 0;
            return this.sessions.filter(s => String(s.tooth_number) === String(num)).length;
        },

        getToothConditionArabic(num) {
            return this.chartData[num]?.condition || 'سليم';
        },

        getToothCardCustomStyle(num) {
            const condName = this.chartData[num]?.condition || 'سليم';
            const condObj = Array.isArray(this.conditionsList) ? this.conditionsList.find(c => c.name === condName) : null;
            if (condObj && condName !== 'سليم') {
                return `background-color: ${condObj.color}18; border-color: ${condObj.color}; color: ${condObj.color};`;
            }
            return 'background-color: #FFFFFF; border-color: #E2E8F0; color: #334155;';
        },

        translateAppointmentStatus(status) {
            const map = { 'Booked': 'محجوز', 'Completed': 'مكتمل', 'Cancelled': 'ملغي', 'No-Show': 'لم يحضر', 'Confirmed': 'محجوز' };
            return map[status] || status;
        },

        getAppointmentStatusBadgeClass(status) {
            switch(status) {
                case 'Completed': return 'bg-emerald-100 text-emerald-800';
                case 'Cancelled': return 'bg-rose-100 text-rose-800';
                case 'No-Show': return 'bg-slate-200 text-slate-800';
                default: return 'bg-teal-100 text-teal-800';
            }
        },

        async initApp() {
            try {
                const resStatus = await fetch('/api/v1/auth/status');
                const dataStatus = await resStatus.json();
                this.systemInitialized = dataStatus.initialized;
            } catch(e) { console.error(e); }

            const savedUser = localStorage.getItem('dental_user');
            if (savedUser) {
                try {
                    this.currentUser = JSON.parse(savedUser);
                    this.isLoggedIn = true;
                    await this.loadInitialData();
                } catch(e) {
                    this.currentUser = null;
                    this.isLoggedIn = false;
                }
            } else {
                this.currentUser = null;
                this.isLoggedIn = false;
            }
        },

        async submitDoctorSetup() {
            if (!this.doctorSetupForm.full_name || !this.doctorSetupForm.username || !this.doctorSetupForm.password) {
                alert("يرجى تعبئة الحقول"); return;
            }
            try {
                const res = await fetch('/api/v1/auth/setup-doctor', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.doctorSetupForm)
                });
                if (res.ok) {
                    const data = await res.json();
                    this.systemInitialized = true;
                    this.currentUser = data.user;
                    this.isLoggedIn = true;
                    localStorage.setItem('dental_user', JSON.stringify(data.user));
                    await this.loadInitialData();
                }
            } catch(e) { console.error(e); }
        },

        async submitLogin() {
            try {
                const res = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(this.loginForm)
                });
                if (res.ok) {
                    const user = await res.json();
                    this.currentUser = user;
                    this.isLoggedIn = true;
                    localStorage.setItem('dental_user', JSON.stringify(user));
                    await this.loadInitialData();
                } else {
                    alert("اسم المستخدم أو كلمة المرور غير صحيحة");
                }
            } catch(e) { console.error(e); }
        },

        logout() {
            localStorage.removeItem('dental_user');
            this.currentUser = null;
            this.isLoggedIn = false;
            this.loginForm = { username: '', password: '' };
        },

        async loadInitialData() {
            try { await this.loadConditions(); } catch(e){}
            try { await this.loadPatients(); } catch(e){}
            try { await this.loadAppointments(); } catch(e){}
            try { await this.loadApprovedLabs(); } catch(e){}
            try { await this.loadLabOrders(); } catch(e){}
            try { await this.loadExpenses(); } catch(e){}
            try { await this.loadFinancialReport(); } catch(e){}
            if (this.currentUser?.role === 'doctor') {
                try { await this.loadUsers(); } catch(e){}
            }

            if (Array.isArray(this.patients) && this.patients.length > 0 && !this.currentPatient) {
                this.selectPatient(this.patients[0]);
            }
        },

        async loadPatients() {
            try {
                const res = await fetch('/api/v1/patients');
                const data = await res.json();
                this.patients = Array.isArray(data) ? data : [];
                if (this.patients.length > 0 && !this.newLabOrder.patient_id) {
                    this.newLabOrder.patient_id = this.patients[0].id;
                    this.appointmentPatientSearch = this.patients[0].full_name;
                }
            } catch(e) { this.patients = []; }
        },

        async loadAppointments() {
            try {
                const res = await fetch('/api/v1/appointments');
                const data = await res.json();
                this.appointments = Array.isArray(data) ? data : [];
            } catch(e) { this.appointments = []; }
        },

        // فتح نافذة السن مع تصفير الإجراءات الإضافية بالكامل
        // ===== مخطط الأسنان بالصورة (تاج + جذر) =====
        safeColor(c) { return /^#[0-9a-fA-F]{3,8}$/.test(c || '') ? c : '#64748B'; },

        partCondition(num, part) {
            const r = this.chartData[num];
            return (part === 'crown' ? r?.crown_condition : r?.root_condition) || 'سليم';
        },

        // الحالة العامة المشتقة (للتوافق): التاج أولاً، وإن كان سليماً فالجذر
        deriveToothCondition(f) {
            const crown = f.crown_condition || 'سليم';
            const root = f.root_condition || 'سليم';
            return crown !== 'سليم' ? crown : root;
        },

        chartSvgInner() {
            const shapes = window.TOOTH_SHAPES || {};
            const V = window.TOOTH_VIEW || { s: 1, labelUpperY: 14, labelLowerY: 350 };
            const colorOf = {};
            (Array.isArray(this.conditionsList) ? this.conditionsList : []).forEach(c => { colorOf[c.name] = this.safeColor(c.color); });
            let out = '';
            for (const num of Object.keys(shapes)) {
                const t = shapes[num];
                out += `<g transform="translate(${t.x},${t.y}) scale(${V.s})">`
                     + `<image href="/static/teeth/t_${num}.png" width="${t.w}" height="${t.h}" style="pointer-events:none"></image>`;
                for (const part of ['crown', 'root']) {
                    const cond = this.partCondition(num, part);
                    const col = colorOf[cond] || '#64748B';
                    const style = cond !== 'سليم'
                        ? `fill:${col};fill-opacity:.55;stroke:${col};stroke-width:2;mix-blend-mode:multiply;`
                        : 'fill:transparent;';
                    out += `<path class="tooth-part" data-tooth="${num}" data-part="${part}" d="${t[part]}" style="${style}"></path>`;
                }
                out += `</g>`;
                const ly = t.upper ? V.labelUpperY : V.labelLowerY;
                const cnt = this.getToothSessionsCount(num);
                out += `<text x="${t.cx}" y="${ly}" text-anchor="middle" class="tooth-num">${num}</text>`;
                if (cnt > 0) {
                    out += `<circle cx="${t.cx + 14}" cy="${ly - 4}" r="6.5" fill="#0f766e"></circle>`
                         + `<text x="${t.cx + 14}" y="${ly - 1}" text-anchor="middle" class="tooth-cnt">${cnt}</text>`;
                }
            }
            return out;
        },

        onChartClick(e) {
            const el = e.target && e.target.closest ? e.target.closest('[data-tooth]') : null;
            if (!el) return;
            this.openToothModal({ number: parseInt(el.dataset.tooth, 10) }, el.dataset.part);
        },

        openToothModal(tooth, part = null) {
            if (!Array.isArray(this.patients) || this.patients.length === 0) {
                alert("يرجى تسجيل مريض أولاً من صفحة سجل المرضى"); return;
            }
            if (!this.currentPatient) {
                this.selectPatient(this.patients[0]);
            }

            this.selectedTooth = tooth;
            const existing = this.chartData[tooth.number];
            const crownCond = existing?.crown_condition || 'سليم';
            const rootCond = existing?.root_condition || 'سليم';
            this.focusPart = part;

            // تصفير الإجراءات الإضافية والملاحظات والتكلفة
            this.toothForm = {
                condition: '',
                crown_condition: crownCond,
                root_condition: rootCond,
                surfaces: existing?.surfaces || '',
                cost: 0,
                notes: existing?.notes || '',
                procedures_summary: '',  // فارغ افتراضياً
                selectedTags: []          // لا يوجد أي وسم مختار افتراضياً
            };
            this.onConditionChange();
        },

        // تفعيل وإلغاء اختيار وسوم الإجراءات الإضافية يدوياً فقط
        toggleProcedureTag(tagName) {
            const idx = this.toothForm.selectedTags.indexOf(tagName);
            if (idx === -1) {
                this.toothForm.selectedTags.push(tagName);
            } else {
                this.toothForm.selectedTags.splice(idx, 1);
            }
            this.toothForm.procedures_summary = this.toothForm.selectedTags.join(' + ');

            // حساب التكلفة بناءً على ما اختاره الطبيب يدوياً فقط
            let total = 0;
            this.toothForm.selectedTags.forEach(t => {
                const cObj = this.conditionsList.find(c => c.name === t);
                if (cObj) total += (cObj.default_cost || 0);
            });
            this.toothForm.cost = total;
        },

        isProcedureTagSelected(tagName) {
            return this.toothForm.selectedTags.includes(tagName);
        },

        // عند تغيير حالة السن على المخطط: لا نتدخل في الإجراءات الإضافية إطلاقاً
        onConditionChange() {
            this.toothForm.condition = this.deriveToothCondition(this.toothForm);
            this.selectedConditionObj = this.conditionsList.find(c => c.name === this.toothForm.condition);
            // إذا لم يختر الطبيب أي وسوم إضافية، نضع تكلفة الحالة الافتراضية
            if (this.toothForm.selectedTags.length === 0 && this.selectedConditionObj) {
                this.toothForm.cost = this.selectedConditionObj.default_cost || 0;
            }
        },

        openLabOrderForCurrentTooth() {
            this.newLabOrder.patient_id = this.currentPatient?.id || (this.patients[0]?.id || '');
            this.newLabOrder.tooth_number = String(this.selectedTooth.number);
            this.newLabOrder.work_type = this.toothForm.condition;
            this.newLabOrder.patient_price = this.toothForm.cost || 0;
            if (this.approvedLabs.length > 0) {
                this.newLabOrder.lab_name = this.approvedLabs[0].name;
            }
            this.showAddLabModal = true;
        },

        async submitLabOrderAPI() {
            if (!this.newLabOrder.patient_id) { alert("يرجى اختيار مريض أولاً"); return; }
            if (!this.newLabOrder.lab_name) { alert("يرجى اختيار المخبر المعتمد من القائمة"); return; }
            if (!this.newLabOrder.work_type) { alert("يرجى تحديد نوع العمل"); return; }

            const payload = {
                patient_id: this.newLabOrder.patient_id,
                lab_name: this.newLabOrder.lab_name,
                tooth_number: this.newLabOrder.tooth_number || null,
                work_type: this.newLabOrder.work_type,
                shade: this.newLabOrder.shade || null,
                sent_date: this.newLabOrder.sent_date,
                expected_date: this.newLabOrder.expected_date ? this.newLabOrder.expected_date : null,
                lab_cost: parseFloat(this.newLabOrder.lab_cost) || 0,
                patient_price: parseFloat(this.newLabOrder.patient_price) || 0,
                notes: this.newLabOrder.notes || null
            };

            const res = await fetch('/api/v1/lab-orders', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                this.showAddLabModal = false;
                await this.loadLabOrders();
                if (this.currentPatient) {
                    await this.loadPatientSessions();
                    await this.loadFinancialSummary();
                }
                alert("تم حفظ وإرسال طلب المخبر بنجاح!");
            } else {
                alert("حدث خطأ أثناء حفظ طلب المخبر.");
            }
        },

        async saveUnifiedToothProcedure() {
            if (this.currentUser?.role !== 'doctor') {
                alert("صلاحية تسجيل الإجراءات السريرية مخصصة للطبيب فقط"); return;
            }
            if (!this.currentPatient) return;

            const toothPayload = {
                patient_id: this.currentPatient.id,
                tooth_number: this.selectedTooth.number,
                condition: this.deriveToothCondition(this.toothForm),
                crown_condition: this.toothForm.crown_condition || 'سليم',
                root_condition: this.toothForm.root_condition || 'سليم',
                surfaces: this.toothForm.surfaces,
                notes: this.toothForm.notes
            };

            const resTooth = await fetch('/api/v1/dental-chart/tooth', {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(toothPayload)
            });

            if (!resTooth.ok) {
                alert("حدث خطأ أثناء حفظ حالة السن"); return;
            }

            const updatedTooth = await resTooth.json();
            this.chartData[updatedTooth.tooth_number] = updatedTooth;

            // تسجيل الجلسة بما اختاره الطبيب
            if (this.deriveToothCondition(this.toothForm) !== 'سليم' || this.toothForm.procedures_summary) {
                const f = this.toothForm;
                const partsTitle = [
                    f.crown_condition && f.crown_condition !== 'سليم' ? `التاج: ${f.crown_condition}` : '',
                    f.root_condition && f.root_condition !== 'سليم' ? `الجذر: ${f.root_condition}` : ''
                ].filter(Boolean).join(' + ');
                const procTitle = f.procedures_summary || partsTitle || this.deriveToothCondition(f);
                const sessionPayload = {
                    patient_id: this.currentPatient.id,
                    tooth_number: String(this.selectedTooth.number),
                    procedure_name: `معالجة السن ${this.selectedTooth.number}: ${procTitle}` + (this.toothForm.surfaces ? ` (${this.toothForm.surfaces})` : ''),
                    cost: parseFloat(this.toothForm.cost) || 0,
                    notes: this.toothForm.notes
                };

                await fetch('/api/v1/clinical-finance/sessions', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(sessionPayload)
                });

                await this.loadPatientSessions();
                await this.loadFinancialSummary();
            }

            this.selectedTooth = null;
        },

        setReportPeriod(period) {
            const today = new Date();
            if (period === 'month') {
                this.reportFilter.start_date = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split('T')[0];
                this.reportFilter.end_date = today.toISOString().split('T')[0];
            } else if (period === 'all') {
                this.reportFilter.start_date = '';
                this.reportFilter.end_date = '';
            }
            this.loadFinancialReport();
        },

        async loadFinancialReport() {
            let url = '/api/v1/clinical-finance/reports';
            const params = [];
            if (this.reportFilter.start_date) params.push(`start_date=${this.reportFilter.start_date}`);
            if (this.reportFilter.end_date) params.push(`end_date=${this.reportFilter.end_date}`);
            if (params.length > 0) url += `?${params.join('&')}`;

            try {
                const res = await fetch(url);
                if (res.ok) {
                    this.clinicReport = await res.json();
                }
            } catch(e) { console.error(e); }
        },

        async submitExpenseAPI() {
            if (!this.newExpense.title || !this.newExpense.amount) {
                alert("يرجى تعبئة البيان والمبلغ"); return;
            }
            const payload = {
                ...this.newExpense,
                amount: parseFloat(this.newExpense.amount)
            };
            const res = await fetch('/api/v1/clinical-finance/expenses', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                this.showAddExpenseModal = false;
                this.newExpense = { title: '', category: 'رواتب وأجور', amount: '', expense_date: new Date().toISOString().split('T')[0], notes: '' };
                await this.loadExpenses();
                await this.loadFinancialReport();
                alert("تم تسجيل المصروف واحتسابه في التقرير المالي!");
            }
        },

        async deleteExpenseAPI(id) {
            if (!confirm("حذف هذا المصروف؟")) return;
            const res = await fetch(`/api/v1/clinical-finance/expenses/${id}`, { method: 'DELETE' });
            if (res.ok) {
                await this.loadExpenses();
                await this.loadFinancialReport();
            }
        },

        handleBackupRestoreUpload(event) {
            this.restoreBackupFile = event.target.files[0];
        },

        async submitRestoreBackupAPI() {
            if (!this.restoreBackupFile) {
                alert("يرجى اختيار ملف نسخة احتياطية أولاً (.db)"); return;
            }
            if (!confirm("تحذير: هل أنت متأكد تماماً من استعادة النسخة الاحتياطية واستبدال البيانات الحالية؟")) return;

            const formData = new FormData();
            formData.append("file", this.restoreBackupFile);

            const res = await fetch('/api/v1/backup/restore', { method: 'POST', body: formData });
            if (res.ok) {
                alert("تمت استعادة قاعدة البيانات بنجاح! سيتم تحديث الصفحة الآن.");
                location.reload();
            } else {
                alert("فشلت عملية استعادة النسخة الاحتياطية.");
            }
        },

        openEditSession(session) {
            this.editSessionForm = { id: session.id, procedure_name: session.procedure_name, cost: session.cost, notes: session.notes || '' };
            this.showEditSessionModal = true;
        },

        async submitEditSessionAPI() {
            const res = await fetch(`/api/v1/clinical-finance/sessions/${this.editSessionForm.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.editSessionForm)
            });
            if (res.ok) {
                this.showEditSessionModal = false;
                await this.loadPatientSessions();
                await this.loadFinancialSummary();
            }
        },

        async deleteSessionAPI(sessionId) {
            if (!confirm("حذف هذه الجلسة؟")) return;
            const res = await fetch(`/api/v1/clinical-finance/sessions/${sessionId}`, { method: 'DELETE' });
            if (res.ok) {
                await this.loadPatientSessions();
                await this.loadFinancialSummary();
            }
        },

        async loadApprovedLabs() {
            try {
                const res = await fetch('/api/v1/lab-orders/labs');
                if (res.ok) {
                    this.approvedLabs = await res.json();
                    if (this.approvedLabs.length > 0 && !this.newLabOrder.lab_name) {
                        this.newLabOrder.lab_name = this.approvedLabs[0].name;
                    }
                }
            } catch(e){}
        },

        async submitAddApprovedLab() {
            if (!this.newApprovedLab.name.trim()) return;
            const res = await fetch('/api/v1/lab-orders/labs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.newApprovedLab)
            });
            if (res.ok) {
                this.newApprovedLab = { name: '', phone: '', specialty: '' };
                await this.loadApprovedLabs();
            }
        },

        async deleteApprovedLab(labId) {
            if (!confirm("حذف المخبر؟")) return;
            const res = await fetch(`/api/v1/lab-orders/labs/${labId}`, { method: 'DELETE' });
            if (res.ok) await this.loadApprovedLabs();
        },

        async loadConditions() {
            try {
                const res = await fetch('/api/v1/conditions');
                if (res.ok) this.conditionsList = await res.json();
            } catch(e){}
        },

        async submitAddConditionAPI() {
            if (!this.newConditionForm.name.trim()) return;
            const res = await fetch('/api/v1/conditions', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: this.newConditionForm.name.trim(),
                    color: this.newConditionForm.color,
                    requires_lab: this.newConditionForm.requires_lab,
                    default_cost: parseFloat(this.newConditionForm.default_cost) || 0
                })
            });
            if (res.ok) {
                this.showAddConditionModal = false;
                this.newConditionForm = { name: '', color: '#3B82F6', requires_lab: false, default_cost: 0 };
                await this.loadConditions();
            }
        },

        openEditCondition(cond) {
            this.editConditionForm = { id: cond.id, name: cond.name, color: cond.color || '#3B82F6', requires_lab: cond.requires_lab || false, default_cost: cond.default_cost || 0 };
            this.showEditConditionModal = true;
        },

        async submitEditConditionAPI() {
            const res = await fetch(`/api/v1/conditions/${this.editConditionForm.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: this.editConditionForm.name.trim(),
                    color: this.editConditionForm.color,
                    requires_lab: this.editConditionForm.requires_lab,
                    default_cost: parseFloat(this.editConditionForm.default_cost) || 0
                })
            });
            if (res.ok) {
                this.showEditConditionModal = false;
                await this.loadConditions();
                alert("تم تحديث الحالة بنجاح!");
            }
        },

        async deleteConditionAPI(id) {
            if (!confirm("حذف هذه الحالة؟")) return;
            const res = await fetch(`/api/v1/conditions/${id}`, { method: 'DELETE' });
            if (res.ok) await this.loadConditions();
        },

        async loadLabOrders() {
            try {
                const res = await fetch('/api/v1/lab-orders');
                if (res.ok) this.labOrders = await res.json();
            } catch(e){}
        },

        async updateLabStatus(id, s) {
            await fetch(`/api/v1/lab-orders/${id}/status`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: s })
            });
            await this.loadLabOrders();
        },

        async deleteLabOrder(id) {
            if (!confirm("حذف السجل؟")) return;
            await fetch(`/api/v1/lab-orders/${id}`, { method: 'DELETE' });
            await this.loadLabOrders();
        },

        translateLabStatus(s) {
            const map = { 'Sent': 'تم الإرسال ⏳', 'In-Lab': 'بالمخبر 🔬', 'Received': 'وصل للعيادة 📦', 'Fitted': 'تم التركيب ✅' };
            return map[s] || s;
        },

        getLabBadgeClass(s) {
            if (s === 'Received') return 'bg-teal-100 text-teal-800';
            if (s === 'Fitted') return 'bg-blue-100 text-blue-800';
            return 'bg-amber-100 text-amber-800';
        },

        openEditAppointment(apt) {
            this.editAppointmentForm = { id: apt.id, appointment_date: apt.appointment_date, appointment_time: apt.appointment_time, notes: apt.notes || '', status: apt.status === 'Confirmed' ? 'Booked' : apt.status };
            this.showEditAppointmentModal = true;
        },

        async submitEditAppointmentAPI() {
            const res = await fetch(`/api/v1/appointments/${this.editAppointmentForm.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.editAppointmentForm)
            });
            if (res.ok) {
                const updated = await res.json();
                const idx = this.appointments.findIndex(a => a.id === updated.id);
                if (idx !== -1) this.appointments[idx] = updated;
                this.showEditAppointmentModal = false;
            }
        },

        async deleteAppointmentAPI(aptId) {
            if (!confirm("حذف هذا الموعد؟")) return;
            const res = await fetch(`/api/v1/appointments/${aptId}`, { method: 'DELETE' });
            if (res.ok) this.appointments = this.appointments.filter(a => a.id !== aptId);
        },

        openEditUser(user) {
            this.editUserForm = { id: user.id, full_name: user.full_name, username: user.username, password: '' };
            this.showEditUserModal = true;
        },

        async submitEditUser() {
            const payload = { full_name: this.editUserForm.full_name, username: this.editUserForm.username };
            if (this.editUserForm.password) payload.password = this.editUserForm.password;
            const res = await fetch(`/api/v1/auth/users/${this.editUserForm.id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                this.showEditUserModal = false;
                await this.loadUsers();
            }
        },

        // ===== منع تكرار الأسماء =====
        askDuplicate(matches, name, mode = 'create') {
            return new Promise(resolve => {
                this.duplicateDialog = { show: true, matches: matches || [], name: name || '', mode, resolve };
            });
        },

        resolveDuplicate(choice) {
            const r = this.duplicateDialog.resolve;
            this.duplicateDialog = { show: false, matches: [], name: '', mode: 'create', resolve: null };
            if (r) r(choice);
        },

        async fetchPatientById(id) {
            let p = this.patients.find(x => x.id === id);
            if (p) return p;
            try {
                const res = await fetch(`/api/v1/patients/${id}`);
                if (res.ok) { p = await res.json(); this.patients.unshift(p); return p; }
            } catch (e) {}
            return null;
        },

        // يُرجع { created } أو { existing } أو null (إلغاء/فشل)
        async postPatient(payload) {
            let url = '/api/v1/patients';
            for (let attempt = 0; attempt < 2; attempt++) {
                const res = await fetch(url, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                if (res.ok) return { created: await res.json() };
                if (res.status === 409) {
                    const err = await res.json().catch(() => ({}));
                    const d = err.detail;
                    if (d && d.code === 'duplicate_name') {
                        const choice = await this.askDuplicate(d.matches, payload.full_name, 'create');
                        if (choice === 'create') { url = '/api/v1/patients?confirm_duplicate=true'; continue; }
                        if (choice && choice.id) {
                            const p = await this.fetchPatientById(choice.id);
                            return p ? { existing: p } : null;
                        }
                        return null;
                    }
                }
                return null;
            }
            return null;
        },

        sendPatientUpdate(id, payload, confirmDup) {
            return fetch(`/api/v1/patients/${id}${confirmDup ? '?confirm_duplicate=true' : ''}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
        },

        // ===== حذف مريض بتأكيد صارم =====
        normName(s) { return (s || '').trim().replace(/\s+/g, ' '); },

        get canConfirmDelete() {
            const d = this.deleteDialog;
            return !!(d.patient && d.impact && d.ack && !d.busy && !d.loading
                && this.normName(d.confirmName) === this.normName(d.patient.full_name));
        },

        async openDeletePatient(patient) {
            this.deleteDialog = { show: true, patient, impact: null, loading: true, confirmName: '', ack: false, busy: false, error: '' };
            try {
                const res = await fetch(`/api/v1/patients/${patient.id}/delete-impact`);
                if (res.ok) this.deleteDialog.impact = await res.json();
                else this.deleteDialog.error = 'تعذر جلب بيانات الملف';
            } catch (e) { this.deleteDialog.error = 'تعذر الاتصال بالخادم'; }
            this.deleteDialog.loading = false;
        },

        closeDeleteDialog() {
            this.deleteDialog = { show: false, patient: null, impact: null, loading: false, confirmName: '', ack: false, busy: false, error: '' };
        },

        async confirmDeletePatient() {
            if (!this.canConfirmDelete) return;
            const d = this.deleteDialog;
            d.busy = true; d.error = '';
            const id = d.patient.id;
            try {
                const res = await fetch(`/api/v1/patients/${id}?confirm_name=${encodeURIComponent(d.confirmName.trim())}`, { method: 'DELETE' });
                if (!res.ok) {
                    const e = await res.json().catch(() => ({}));
                    d.error = typeof e.detail === 'string' ? e.detail : 'فشل الحذف';
                    d.busy = false;
                    return;
                }
            } catch (e) { d.error = 'تعذر الاتصال بالخادم'; d.busy = false; return; }

            this.patients = this.patients.filter(p => p.id !== id);
            if (this.currentPatient && this.currentPatient.id === id) {
                if (this.patients.length) {
                    this.selectPatient(this.patients[0]);
                } else {
                    this.currentPatient = null;
                    this.chartData = {};
                    this.sessions = [];
                    this.currentPatientXRays = [];
                    this.financeSummary = { total_cost: 0, total_paid: 0, balance_due: 0, payments: [] };
                }
            }
            this.closeDeleteDialog();
            await this.loadAppointments();
        },

        // ===== سجل جلسات المريض الكامل =====
        fmtMoney(v) { return (Number(v) || 0).toLocaleString('en-US'); },
        fmtDateTime(v) { return (v || '').replace('T', ' ').slice(0, 16); },

        get historySessions() {
            const q = (this.historyFilter.q || '').trim();
            const tooth = this.historyFilter.tooth;
            return [...(this.sessions || [])]
                .filter(s => !tooth || String(s.tooth_number) === String(tooth))
                .filter(s => !q || (((s.procedure_name || '') + ' ' + (s.notes || '')).includes(q)))
                .sort((a, b) => String(b.session_date).localeCompare(String(a.session_date))
                    || String(b.created_at || '').localeCompare(String(a.created_at || '')));
        },

        get historyShownTotal() {
            return this.historySessions.reduce((t, s) => t + (Number(s.cost) || 0), 0);
        },

        get historyTeethOptions() {
            return [...new Set((this.sessions || []).map(s => s.tooth_number).filter(Boolean))].sort();
        },

        toothStatusText(num) {
            const r = this.chartData[num];
            if (!r) return '';
            const parts = [];
            if (r.crown_condition && r.crown_condition !== 'سليم') parts.push('تاج: ' + r.crown_condition);
            if (r.root_condition && r.root_condition !== 'سليم') parts.push('جذر: ' + r.root_condition);
            return parts.join(' | ');
        },

        openEditPatient(patient) {
            this.editPatientForm = { id: patient.id, full_name: patient.full_name, phone: patient.phone, gender: patient.gender || '', age: patient.age || '', allergies: patient.allergies || '', medical_notes: patient.medical_notes || '' };
            this.showEditPatientModal = true;
        },

        async submitEditPatientAPI() {
            const payload = { ...this.editPatientForm };
            delete payload.id;
            payload.age = payload.age ? parseInt(payload.age) : null;
            if (!payload.gender) payload.gender = null;
            let res = await this.sendPatientUpdate(this.editPatientForm.id, payload, false);
            if (res.status === 409) {
                const err = await res.json().catch(() => ({}));
                const d = err.detail;
                if (!(d && d.code === 'duplicate_name')) return;
                const choice = await this.askDuplicate(d.matches, payload.full_name, 'edit');
                if (choice !== 'create') return;
                res = await this.sendPatientUpdate(this.editPatientForm.id, payload, true);
            }
            if (res.ok) {
                const updated = await res.json();
                const idx = this.patients.findIndex(p => p.id === updated.id);
                if (idx !== -1) this.patients[idx] = updated;
                if (this.currentPatient && this.currentPatient.id === updated.id) this.currentPatient = updated;
                this.showEditPatientModal = false;
            }
        },

        async deleteXRayAPI(xrayId) {
            if (!confirm("حذف الصورة؟")) return;
            const res = await fetch(`/api/v1/xrays/${xrayId}`, { method: 'DELETE' });
            if (res.ok) await this.loadPatientXRays();
        },

        async loadPatientXRays() {
            if (!this.currentPatient) return;
            try {
                const res = await fetch(`/api/v1/xrays/patients/${this.currentPatient.id}`);
                if (res.ok) this.currentPatientXRays = await res.json();
            } catch(e){}
        },

        handleXRayUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (e) => { this.newXRay.image_data = e.target.result; };
            reader.readAsDataURL(file);
        },

        async submitXRayAPI() {
            if (!this.newXRay.image_data) return;
            const payload = { patient_id: this.currentPatient.id, title: this.newXRay.title || 'صورة شعاعية', image_data: this.newXRay.image_data };
            const res = await fetch('/api/v1/xrays', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                this.showAddXRayModal = false;
                this.newXRay = { title: '', image_data: '', notes: '' };
                await this.loadPatientXRays();
            }
        },

        viewXRay(img) { this.viewingXRayImg = img; },

        async loadExpenses() {
            try {
                const res = await fetch('/api/v1/clinical-finance/expenses');
                if (res.ok) this.clinicExpenses = await res.json();
            } catch(e){}
        },

        formatPatientId(id) { return id ? '#PAT-' + id.substring(0, 6).toUpperCase() : ''; },
        getPatientName(id) { const p = Array.isArray(this.patients) ? this.patients.find(x => x.id === id) : null; return p ? p.full_name : 'مريض غير مسجل'; },

        selectPatient(patient) {
            if (!patient) return;
            this.currentPatient = patient;
            this.newAppointment.patient_id = patient.id;
            this.appointmentPatientSearch = patient.full_name;
            this.newLabOrder.patient_id = patient.id;
            this.loadPatientChart();
            this.loadPatientSessions();
            this.loadFinancialSummary();
            this.loadPatientXRays();
        },

        async loadPatientSessions() {
            if (!this.currentPatient) return;
            try {
                const res = await fetch(`/api/v1/clinical-finance/sessions/patients/${this.currentPatient.id}`);
                if (res.ok) this.sessions = await res.json();
            } catch(e){}
        },

        async loadFinancialSummary() {
            if (!this.currentPatient) return;
            try {
                const res = await fetch(`/api/v1/clinical-finance/finance/summary/${this.currentPatient.id}`);
                if (res.ok) this.financeSummary = await res.json();
            } catch(e){}
        },

        async loadPatientChart() {
            if (!this.currentPatient) return;
            try {
                const res = await fetch(`/api/v1/dental-chart/patients/${this.currentPatient.id}`);
                if (res.ok) {
                    const records = await res.json();
                    this.chartData = {};
                    records.forEach(r => { this.chartData[r.tooth_number] = r; });
                }
            } catch(e){}
        },

        async savePaymentAPI() {
            if (!this.newPayment.amount || this.newPayment.amount <= 0) return;
            const payload = { patient_id: this.currentPatient.id, amount: parseFloat(this.newPayment.amount), payment_method: this.newPayment.payment_method, notes: this.newPayment.notes };
            const res = await fetch('/api/v1/clinical-finance/payments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (res.ok) {
                this.showAddPaymentModal = false;
                this.newPayment = { amount: '', payment_method: 'Cash', notes: '' };
                await this.loadFinancialSummary();
                await this.loadFinancialReport();
            }
        },

        async createPatientAPI() {
            if (!this.newPatient.full_name || !this.newPatient.phone) return;
            const payload = { ...this.newPatient };
            payload.age = payload.age ? parseInt(payload.age) : null;
            if (!payload.gender) payload.gender = null;
            const r = await this.postPatient(payload);
            if (!r) return;
            if (r.created) this.patients.unshift(r.created);
            this.showAddPatientModal = false;
            this.newPatient = { full_name: '', phone: '', gender: '', age: '', allergies: '' };
            this.selectPatient(r.created || r.existing);
        },

        async handleBookAppointment() {
            if (this.appointmentMode === 'new') {
                if (!this.quickPatient.full_name || !this.quickPatient.phone) return;
                const pPayload = { ...this.quickPatient };
                pPayload.age = pPayload.age ? parseInt(pPayload.age) : null;
                if (!pPayload.gender) pPayload.gender = null;

                const r = await this.postPatient(pPayload);
                if (!r) return;
                const created = r.created || r.existing;
                if (r.created) this.patients.push(r.created);
                this.newAppointment.patient_id = created.id;
                this.selectPatient(created);
            }
            const resApt = await fetch('/api/v1/appointments', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.newAppointment)
            });
            if (resApt.ok) {
                const apt = await resApt.json();
                this.appointments.unshift(apt);
                this.showAddAppointmentModal = false;
                this.quickPatient = { full_name: '', phone: '', gender: '', age: '' };
                this.newAppointment.notes = '';
                alert("تم حجز الموعد بنجاح!");
            }
        },

        async loadUsers() {
            try {
                const res = await fetch('/api/v1/auth/users');
                if (res.ok) this.usersList = await res.json();
            } catch(e){}
        },

        async submitCreateUser() {
            if (!this.newUserForm.full_name || !this.newUserForm.username || !this.newUserForm.password) return;
            const res = await fetch('/api/v1/auth/users', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.newUserForm)
            });
            if (res.ok) {
                this.showAddUserModal = false;
                this.newUserForm = { full_name: '', username: '', password: '', role: 'secretary' };
                await this.loadUsers();
            }
        },

        async deleteUser(user) {
            if (!confirm(`حذف المستخدم "${user.full_name}"؟`)) return;
            const res = await fetch(`/api/v1/auth/users/${user.id}`, { method: 'DELETE' });
            if (res.ok) await this.loadUsers();
        }
    }
}
