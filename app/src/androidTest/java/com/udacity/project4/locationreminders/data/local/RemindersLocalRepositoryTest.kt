package com.udacity.project4.locationreminders.data.local

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import androidx.room.Room
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.filters.MediumTest
import com.udacity.project4.locationreminders.data.dto.ReminderDTO
import com.udacity.project4.locationreminders.data.dto.Result
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.runBlocking
import org.hamcrest.CoreMatchers.`is`
import org.hamcrest.CoreMatchers.instanceOf
import org.hamcrest.MatcherAssert.assertThat
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith

@ExperimentalCoroutinesApi
@RunWith(AndroidJUnit4::class)
@MediumTest
class RemindersLocalRepositoryTest {
    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    private lateinit var database: RemindersDatabase
    private lateinit var repository: RemindersLocalRepository

    @Before
    fun initRepository() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            RemindersDatabase::class.java
        ).allowMainThreadQueries().build()
        repository = RemindersLocalRepository(database.reminderDao(), Dispatchers.Main)
    }

    @After
    fun cleanupDb() = database.close()

    @Test
    fun saveReminderAndGetReminder_returnsSuccess() = runBlocking {
        val reminder = ReminderDTO("Title", "Description", "Location", 1.0, 2.0, "id-1")

        repository.saveReminder(reminder)
        val result = repository.getReminder("id-1")

        assertThat(result, instanceOf(Result.Success::class.java))
        assertThat((result as Result.Success).data.title, `is`("Title"))
    }

    @Test
    fun getMissingReminder_returnsError() = runBlocking {
        val result = repository.getReminder("missing")

        assertThat(result, instanceOf(Result.Error::class.java))
    }

    @Test
    fun deleteAllReminders_removesSavedRows() = runBlocking {
        repository.saveReminder(ReminderDTO("Title", "Description", "Location", 1.0, 2.0, "id-1"))

        repository.deleteAllReminders()
        val result = repository.getReminders()

        assertThat((result as Result.Success).data.isEmpty(), `is`(true))
    }
}
