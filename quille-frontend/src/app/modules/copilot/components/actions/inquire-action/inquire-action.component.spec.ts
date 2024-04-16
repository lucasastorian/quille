import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InquireActionComponent } from './inquire-action.component';

describe('InquireActionComponent', () => {
  let component: InquireActionComponent;
  let fixture: ComponentFixture<InquireActionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InquireActionComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(InquireActionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
